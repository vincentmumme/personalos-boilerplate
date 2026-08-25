#!/usr/bin/env python3
"""Dependency-free runtime for the registry-owned PersonalOS pos-v1 contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import secrets
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

_TIME_CONTEXT_DIR = Path(__file__).resolve().parent
if str(_TIME_CONTEXT_DIR) not in sys.path:
    sys.path.insert(0, str(_TIME_CONTEXT_DIR))
from time_context import local_date


FOUNDATION_ORDER = ["schema_version", "id", "type", "title", "created", "updated"]
SKILL_RUNTIME_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_RUNTIME_NAME_MAX = 64
SKILL_RUNTIME_DESCRIPTION_MAX = 1024
WIKILINK_RE = re.compile(r"^\[\[[^\]\n]+\]\]$")
LOWER_KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
FENCED_BLOCK_RE = re.compile(r"^```[^\n]*\n.*?^```\s*$", re.M | re.S)


class ContractError(ValueError):
    pass


@dataclass
class Finding:
    level: str
    code: str
    path: str
    message: str
    remediation: str


def parse_scalar(raw: str):
    value = raw.strip()
    if value == "":
        raise ContractError("Empty scalar is not allowed; omit optional values.")
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            inner = value[1:-1].strip()
            if not inner:
                return []
            items = [item.strip() for item in inner.split(",")]
            if any(not item or any(char in item for char in "[]{}\"") for item in items):
                raise ContractError("Non-scalar inline list values must use JSON string syntax.")
            return items
    if value in {"{}"} or value.startswith(("{", '"')):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ContractError(f"Inline maps and quoted strings must use JSON syntax: {exc}") from exc
    if value in {"true", "false"}:
        return value == "true"
    if value == "null":
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def load_restricted_yaml_text(text: str) -> tuple[dict, list[str]]:
    """Parse the deliberately small registry/frontmatter YAML dialect.

    It supports indentation-based mappings and JSON-syntax inline arrays. Block
    sequences, anchors, tags, folded values and arbitrary YAML objects are out of
    contract by design.
    """

    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    top_level_keys: list[str] = []

    for lineno, original in enumerate(text.splitlines(), start=1):
        if not original.strip() or original.lstrip().startswith("#"):
            continue
        if "\t" in original[: len(original) - len(original.lstrip())]:
            raise ContractError(f"Line {lineno}: indentation must use spaces.")
        indent = len(original) - len(original.lstrip(" "))
        if indent % 2:
            raise ContractError(f"Line {lineno}: indentation must be a multiple of two.")
        line = original.strip()
        if line.startswith("-"):
            raise ContractError(f"Line {lineno}: block sequences are not allowed; use an inline JSON list.")
        if ":" not in line:
            raise ContractError(f"Line {lineno}: expected `key: value`.")
        key, raw = line.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]+", key):
            raise ContractError(f"Line {lineno}: invalid key `{key}`.")

        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if key in parent:
            raise ContractError(f"Line {lineno}: duplicate key `{key}`.")
        if indent == 0:
            top_level_keys.append(key)

        if raw.strip() == "":
            child: dict = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = parse_scalar(raw)

    return root, top_level_keys


def load_restricted_yaml(path: Path) -> dict:
    data, _ = load_restricted_yaml_text(path.read_text(encoding="utf-8"))
    return data


def split_markdown(text: str) -> tuple[dict, list[str], str]:
    if not text.startswith("---\n"):
        raise ContractError("Record must start with a frontmatter delimiter.")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ContractError("Record has no closing frontmatter delimiter.")
    frontmatter, keys = load_restricted_yaml_text(text[4:end])
    return frontmatter, keys, text[end + 5 :]


def uuid7() -> str:
    timestamp_ms = int(time.time() * 1000) & ((1 << 48) - 1)
    random_a = secrets.randbits(12)
    random_b = secrets.randbits(62)
    value = timestamp_ms << 80
    value |= 0x7 << 76
    value |= random_a << 64
    value |= 0b10 << 62
    value |= random_b
    return str(uuid.UUID(int=value))


def is_uuid7(value: object) -> bool:
    if not isinstance(value, str) or value != value.lower():
        return False
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        return False
    return parsed.version == 7 and parsed.variant == uuid.RFC_4122 and str(parsed) == value


def valid_date(value: object) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def valid_datetime(value: object) -> bool:
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})",
        value,
    ):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def valid_iana_timezone(value: object) -> bool:
    if not isinstance(value, str) or not value.strip() or "\n" in value:
        return False
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError):
        return False
    return True


def target_from_wikilink(value: str) -> str:
    inner = value[2:-2]
    return inner.split("|", 1)[0].split("#", 1)[0].strip()


class Contract:
    def __init__(self, vault_root: Path):
        self.vault_root = vault_root.resolve()
        self.model_root = self.vault_root / "system" / "data-model"
        self.registry = load_restricted_yaml(self.model_root / "registry.yaml")
        self.foundation = load_restricted_yaml(self.model_root / self.registry["foundation"])
        self.governance = load_restricted_yaml(self.model_root / self.registry["governance"])
        self.deprecations = load_restricted_yaml(self.model_root / self.registry["deprecations"])
        self.page_shapes = {
            name: load_restricted_yaml(self.model_root / relative)
            for name, relative in self.registry["page_shapes"].items()
        }
        self.modules = {
            name: load_restricted_yaml(self.model_root / relative)
            for name, relative in self.registry["modules"].items()
        }
        self.profiles = {
            name: load_restricted_yaml(self.model_root / relative)
            for name, relative in self.registry["profiles"].items()
        }
        self.field_owners: dict[str, str] = {}
        self.field_definitions: dict[str, dict] = {}
        self._register_fields("foundation", self.foundation.get("fields", {}))
        for module_name, module in self.modules.items():
            self._register_fields(f"module:{module_name}", module.get("fields", {}))
        for profile_name, profile in self.profiles.items():
            self._register_fields(f"profile:{profile_name}", profile.get("fields", {}))
        self._validate_registry()

    def _register_fields(self, owner: str, fields: dict) -> None:
        for field, definition in fields.items():
            if field in self.field_owners:
                previous = self.field_owners[field]
                raise ContractError(f"Field `{field}` is defined by both {previous} and {owner}.")
            self.field_owners[field] = owner
            self.field_definitions[field] = definition

    def _validate_registry(self) -> None:
        if self.foundation.get("field_order") != FOUNDATION_ORDER:
            raise ContractError("Foundation field order differs from the locked six-field contract.")
        if self.governance.get("contract") != self.registry.get("contract"):
            raise ContractError("Governance contract does not match the Registry contract.")
        if self.deprecations.get("contract") != self.registry.get("contract"):
            raise ContractError("Deprecation registry does not match the Registry contract.")
        for version_field, value in {
            "registry_version": self.registry.get("registry_version"),
            "governance_version": self.governance.get("governance_version"),
        }.items():
            if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
                raise ContractError(f"`{version_field}` must use semantic x.y.z versioning.")

        profile_states = self.registry.get("profile_states", {})
        if set(profile_states) != set(self.profiles):
            missing = sorted(set(self.profiles) - set(profile_states))
            extra = sorted(set(profile_states) - set(self.profiles))
            raise ContractError(f"Profile state registry mismatch; missing={missing}, extra={extra}.")
        allowed_profile_states = set(self.governance.get("profile_states", []))
        invalid_states = {name: state for name, state in profile_states.items() if state not in allowed_profile_states}
        if invalid_states:
            raise ContractError(f"Profiles use unknown activation states: {invalid_states}.")

        closed_shapes = set(self.governance.get("closed_page_shapes", []))
        page_shape_required = set(self.governance["admission"]["page_shape"]["required_keys"])
        for shape_name, shape in self.page_shapes.items():
            if shape_name not in closed_shapes:
                raise ContractError(f"Page shape `{shape_name}` is outside the closed Page Shape catalog.")
            missing = sorted(page_shape_required - set(shape))
            if missing:
                raise ContractError(f"Page shape `{shape_name}` is missing admission keys: {missing}.")

        module_required = set(self.governance["admission"]["module"]["required_keys"])
        allowed_module_states = set(self.governance.get("module_states", []))
        minimum_consumers = int(self.governance["admission"]["module"].get("minimum_active_consumers", 2))
        for module_name, module in self.modules.items():
            if module.get("name") != module_name:
                raise ContractError(f"Module key/name mismatch for `{module_name}`.")
            missing = sorted(module_required - set(module))
            if missing:
                raise ContractError(f"Module `{module_name}` is missing admission keys: {missing}.")
            state = module.get("admission_state")
            if state not in allowed_module_states:
                raise ContractError(f"Module `{module_name}` uses unknown admission state `{state}`.")
            consumers = [
                name
                for name, profile in self.profiles.items()
                if module_name in profile.get("required_modules", []) + profile.get("optional_modules", [])
            ]
            if state == "active" and len(consumers) < minimum_consumers:
                raise ContractError(
                    f"Active module `{module_name}` has {len(consumers)} registered consumer(s); minimum is {minimum_consumers}."
                )
            if state == "pilot" and len(consumers) < minimum_consumers and not module.get("planned_consumers"):
                raise ContractError(f"Pilot module `{module_name}` needs planned consumers while below the active threshold.")

        profile_required = set(self.governance["admission"]["profile"]["required_keys"])
        admission_evidence_required = set(
            self.governance["admission"]["profile"].get("admission_evidence_keys", [])
        )
        for profile_name, profile in self.profiles.items():
            if profile.get("name") != profile_name:
                raise ContractError(f"Profile key/name mismatch for `{profile_name}`.")
            missing = sorted(profile_required - set(profile))
            if missing:
                raise ContractError(f"Profile `{profile_name}` is missing admission keys: {missing}.")
            shape = profile.get("page_shape")
            if shape not in self.page_shapes:
                raise ContractError(f"Profile `{profile_name}` references unknown page shape `{shape}`.")
            try:
                re.compile(profile.get("path_pattern", ""))
            except re.error as exc:
                raise ContractError(f"Profile `{profile_name}` has invalid path regex: {exc}") from exc
            parent_record = profile.get("parent_record")
            if parent_record:
                required_parent_keys = {"when_path_pattern", "required_path_template", "required_profile"}
                missing_parent_keys = sorted(required_parent_keys - set(parent_record))
                if missing_parent_keys:
                    raise ContractError(
                        f"Profile `{profile_name}` parent_record is missing keys: {missing_parent_keys}."
                    )
                try:
                    parent_pattern = re.compile(parent_record["when_path_pattern"])
                except re.error as exc:
                    raise ContractError(f"Profile `{profile_name}` has invalid parent path regex: {exc}") from exc
                placeholders = set(re.findall(r"\{([a-z_][a-z0-9_]*)\}", parent_record["required_path_template"]))
                unknown_placeholders = placeholders - set(parent_pattern.groupindex)
                if unknown_placeholders:
                    raise ContractError(
                        f"Profile `{profile_name}` parent path template uses unknown groups: {sorted(unknown_placeholders)}."
                    )
                if parent_record["required_profile"] not in self.profiles:
                    raise ContractError(
                        f"Profile `{profile_name}` parent_record references unknown profile `{parent_record['required_profile']}`."
                    )
            template = self.vault_root / profile.get("template", "")
            if not template.is_file():
                raise ContractError(f"Profile `{profile_name}` template does not exist: {profile.get('template')}")
            admission = profile.get("admission", {})
            missing_evidence = sorted(admission_evidence_required - set(admission))
            if missing_evidence:
                raise ContractError(f"Profile `{profile_name}` is missing admission evidence: {missing_evidence}.")
            for artifact_key in ("positive_fixture", "negative_fixture", "validator_test", "migration_mapping"):
                artifact = self.vault_root / admission.get(artifact_key, "")
                if not artifact.is_file():
                    raise ContractError(
                        f"Profile `{profile_name}` admission artifact `{artifact_key}` does not exist: {admission.get(artifact_key)}"
                    )
            modules = profile.get("required_modules", []) + profile.get("optional_modules", [])
            for module in modules:
                if module not in self.modules:
                    raise ContractError(f"Profile `{profile_name}` references unknown module `{module}`.")
            permitted_fields = set(profile.get("fields", {}))
            for module in modules:
                permitted_fields.update(self.modules[module].get("fields", {}))
            declared = set(profile.get("required_fields", [])) | set(profile.get("optional_fields", []))
            unknown = declared - permitted_fields
            if unknown:
                raise ContractError(
                    f"Profile `{profile_name}` declares fields not owned by itself or a module: {sorted(unknown)}"
                )
            overlap = set(profile.get("required_fields", [])) & set(profile.get("optional_fields", []))
            if overlap:
                raise ContractError(f"Profile `{profile_name}` declares required/optional field overlap: {sorted(overlap)}")
            declared_sections = profile.get("required_sections", [])
            ordered_sections = profile.get("section_order", [])
            if any(section not in ordered_sections for section in declared_sections):
                raise ContractError(f"Profile `{profile_name}` section_order omits a required section.")
            for rule_name, rule in profile.get("conditional_rules", {}).items():
                undeclared = set(rule.get("require_fields", [])) - declared
                if undeclared:
                    raise ContractError(
                        f"Profile `{profile_name}` conditional `{rule_name}` requires undeclared fields: {sorted(undeclared)}"
                    )
                forbidden_undeclared = set(rule.get("forbid_fields", [])) - declared
                if forbidden_undeclared:
                    raise ContractError(
                        f"Profile `{profile_name}` conditional `{rule_name}` forbids undeclared fields: {sorted(forbidden_undeclared)}"
                    )
                overlap = set(rule.get("require_fields", [])) & set(rule.get("forbid_fields", []))
                if overlap:
                    raise ContractError(
                        f"Profile `{profile_name}` conditional `{rule_name}` both requires and forbids: {sorted(overlap)}"
                    )
                trigger = rule.get("when_present") or rule.get("when_field")
                if trigger not in declared:
                    raise ContractError(
                        f"Profile `{profile_name}` conditional `{rule_name}` uses undeclared trigger `{trigger}`."
                    )
            path_date_field = profile.get("path_date_field")
            if path_date_field and path_date_field not in declared:
                raise ContractError(
                    f"Profile `{profile_name}` path_date_field references undeclared field `{path_date_field}`."
                )
            path_date_prefix_template = profile.get("path_date_prefix_template")
            if path_date_prefix_template:
                if not path_date_field:
                    raise ContractError(
                        f"Profile `{profile_name}` defines path_date_prefix_template without path_date_field."
                    )
                placeholders = set(re.findall(r"\{([a-z_]+)\}", path_date_prefix_template))
                unknown_placeholders = placeholders - {"date", "year", "month", "day"}
                if unknown_placeholders:
                    raise ContractError(
                        f"Profile `{profile_name}` path_date_prefix_template uses unknown placeholders: {sorted(unknown_placeholders)}."
                    )
            path_date_group = profile.get("path_date_group")
            if path_date_group:
                if not path_date_field:
                    raise ContractError(
                        f"Profile `{profile_name}` defines path_date_group without path_date_field."
                    )
                pattern_groups = re.compile(profile.get("path_pattern", "")).groupindex
                if path_date_group not in pattern_groups:
                    raise ContractError(
                        f"Profile `{profile_name}` path_date_group `{path_date_group}` is not a named path_pattern group."
                    )

        field_required = set(self.governance["admission"]["field"]["required_keys"])
        for field, definition in self.field_definitions.items():
            missing = sorted(field_required - set(definition))
            if missing:
                raise ContractError(f"Field `{field}` is missing admission keys: {missing}.")
            if definition.get("datatype") == "enum" and not definition.get("profile_constrained") and not definition.get("enum"):
                raise ContractError(f"Enum field `{field}` has no values and is not profile-constrained.")

        for profile_name, state in profile_states.items():
            if state == "deprecated" and profile_name not in self.deprecations.get("profiles", {}):
                raise ContractError(f"Deprecated profile `{profile_name}` has no deprecation contract.")
        for module_name, module in self.modules.items():
            if module.get("admission_state") == "deprecated" and module_name not in self.deprecations.get("modules", {}):
                raise ContractError(f"Deprecated module `{module_name}` has no deprecation contract.")

        for profile_name, profile in self.profiles.items():
            admission = profile["admission"]
            positive = (self.vault_root / admission["positive_fixture"]).read_text(encoding="utf-8")
            positive_findings = self.validate_text(
                positive,
                admission["positive_logical_path"],
                resolve_relations=False,
            )
            if any(item.level == "fail" for item in positive_findings):
                codes = sorted({item.code for item in positive_findings if item.level == "fail"})
                raise ContractError(f"Profile `{profile_name}` positive fixture fails admission: {codes}.")
            negative = (self.vault_root / admission["negative_fixture"]).read_text(encoding="utf-8")
            negative_findings = self.validate_text(
                negative,
                admission["negative_logical_path"],
                resolve_relations=False,
            )
            if not any(item.level == "fail" for item in negative_findings):
                raise ContractError(f"Profile `{profile_name}` negative fixture does not fail validation.")

    def writable_profiles(self) -> list[str]:
        writable_states = set(self.governance.get("writable_profile_states", []))
        return sorted(name for name, state in self.registry.get("profile_states", {}).items() if state in writable_states)

    def profile_fields(self, profile_name: str) -> tuple[dict[str, dict], set[str], set[str]]:
        profile = self.profiles[profile_name]
        required = set(self.foundation["required_fields"]) | set(profile.get("required_fields", []))
        optional = set(profile.get("optional_fields", []))
        definitions = {field: self.field_definitions[field] for field in required | optional}
        return definitions, required, optional

    def resolve_link(self, value: str) -> tuple[Path | None, dict | None]:
        target = target_from_wikilink(value)
        candidates = []
        direct = self.vault_root / target
        candidates.extend([direct, direct.with_suffix(".md")])
        if "/" not in target:
            candidates.append(self.vault_root / f"{target}.md")
        for candidate in candidates:
            if candidate.is_file():
                try:
                    fm, _, _ = split_markdown(candidate.read_text(encoding="utf-8"))
                except ContractError:
                    return candidate, None
                return candidate, self._project_skill_metadata(fm)
        return None, None

    @staticmethod
    def _project_skill_metadata(frontmatter: dict) -> dict:
        metadata = frontmatter.get("metadata")
        if not isinstance(metadata, dict) or metadata.get("pos_schema_version") != "pos-v1":
            return frontmatter
        return {
            key.removeprefix("pos_"): value
            for key, value in metadata.items()
            if key.startswith("pos_")
        }

    def _finding(self, level: str, code: str, path: str, message: str, remediation: str) -> Finding:
        return Finding(level, code, path, message, remediation)

    def _validate_field(self, field: str, value, definition: dict, path: str) -> list[Finding]:
        findings: list[Finding] = []
        datatype = definition.get("datatype")

        def fail(message: str, remediation: str) -> None:
            findings.append(self._finding("fail", "pos_v1_invalid_field", path, f"`{field}` {message}", remediation))

        if value is None or value == "" or value == []:
            fail("must not be null or empty.", "Omit an optional field or provide a meaningful value.")
            return findings
        if isinstance(value, dict):
            fail("must not contain a nested map.", "Move structured data to the body or companion data.")
            return findings

        if datatype == "literal" and value != definition.get("value"):
            fail(f"must equal `{definition.get('value')}`.", "Use the registered literal value.")
        elif datatype == "uuidv7" and not is_uuid7(value):
            fail("must be a lowercase UUIDv7.", "Generate the ID with `pos_v1.py new-id`.")
        elif datatype == "profile-key" and (not isinstance(value, str) or not LOWER_KEBAB_RE.fullmatch(value)):
            fail("must be a lower-kebab-case profile key.", "Use a registered profile key.")
        elif datatype == "profile-key" and definition.get("registered_profile") and value not in self.profiles:
            fail("must name a registered profile.", "Register the target profile before referencing it.")
        elif datatype == "lower-kebab" and (not isinstance(value, str) or not LOWER_KEBAB_RE.fullmatch(value)):
            fail("must be a lower-kebab-case value.", "Use lowercase words separated by single hyphens.")
        elif datatype == "profile-key-list":
            if not isinstance(value, list) or len(value) < int(definition.get("min_items", 1)):
                fail("must be a non-empty list of profile keys.", "Use a non-empty inline list of registered lower-kebab-case profile keys.")
            elif any(not isinstance(item, str) or not LOWER_KEBAB_RE.fullmatch(item) for item in value):
                fail("contains a value that is not a lower-kebab-case profile key.", "Use only lower-kebab-case profile keys.")
            elif definition.get("registered_profile") and any(item not in self.profiles for item in value):
                unknown = sorted(item for item in value if item not in self.profiles)
                fail(f"contains unregistered profiles: {unknown}.", "Register every referenced profile before declaring capability I/O.")
        elif datatype == "plain-text" and (not isinstance(value, str) or "\n" in value or not value.strip()):
            fail("must be non-empty one-line plain text.", "Use a one-line display title.")
        elif datatype == "plain-text" and definition.get("iana_timezone") and not valid_iana_timezone(value):
            fail("must be a valid IANA timezone.", "Use a zone such as `Europe/Berlin`, `Asia/Makassar` or `UTC`.")
        elif datatype == "plain-text" and definition.get("pattern") and not re.fullmatch(definition["pattern"], value):
            fail(f"must match `{definition['pattern']}`.", "Use the registered one-line value format.")
        elif datatype == "plain-text-list":
            if not isinstance(value, list) or len(value) < int(definition.get("min_items", 1)):
                fail("must be a non-empty list of one-line plain-text values.", "Use a non-empty inline JSON list of one-line strings.")
            elif any(not isinstance(item, str) or "\n" in item or not item.strip() for item in value):
                fail("contains an empty or multiline value.", "Use only non-empty one-line strings.")
        elif datatype == "integer" and (
            not isinstance(value, int)
            or isinstance(value, bool)
            or (definition.get("minimum") is not None and value < int(definition["minimum"]))
            or (definition.get("maximum") is not None and value > int(definition["maximum"]))
        ):
            fail("must be an integer inside the registered bounds.", "Use an unquoted whole number within the allowed range.")
        elif datatype == "decimal" and (
            not isinstance(value, str)
            or not re.fullmatch(r"-?(?:0|[1-9]\d*)(?:\.\d+)?", value)
        ):
            fail("must be a canonical decimal string.", "Use a quoted decimal such as `\"1190.00\"` without a currency symbol.")
        elif datatype == "date" and not valid_date(value):
            fail("must be a valid YYYY-MM-DD date.", "Use a valid ISO calendar date.")
        elif datatype == "datetime" and not valid_datetime(value):
            fail("must be an RFC 3339 timestamp with seconds and UTC offset.", "Use `YYYY-MM-DDTHH:MM:SS+HH:MM` or a `Z` suffix.")
        elif datatype == "semver" and (
            not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", value)
        ):
            fail("must use semantic x.y.z versioning.", "Use a semantic version such as `1.0.0`.")
        elif datatype == "boolean" and not isinstance(value, bool):
            fail("must be a boolean.", "Use the unquoted literal `true` or `false`.")
        elif datatype == "enum" and value not in definition.get("enum", []):
            fail(f"must be one of {definition.get('enum', [])}.", "Use a registered enum value.")
        elif datatype == "uri":
            parsed = urlparse(value) if isinstance(value, str) else None
            if parsed is None or not parsed.scheme:
                fail("must be an absolute URI.", "Use a URI with a scheme, or omit the optional field.")
        elif datatype == "wikilink" and (not isinstance(value, str) or not WIKILINK_RE.fullmatch(value)):
            fail("must be one quoted Obsidian wikilink value.", "Use a YAML-quoted value such as `\"[[path/to/record]]\"`.")
        elif datatype == "wikilink-list":
            if not isinstance(value, list) or len(value) < int(definition.get("min_items", 1)):
                fail("must be a non-empty inline list of wikilinks.", "Use an inline list such as `[\"[[path/to/record]]\"]`.")
            elif any(not isinstance(item, str) or not WIKILINK_RE.fullmatch(item) for item in value):
                fail("contains a value that is not an Obsidian wikilink.", "Quote every wikilink inside the inline list.")
        return findings

    def validate_text(self, text: str, relative_path: str, *, resolve_relations: bool = True) -> list[Finding]:
        path = relative_path.replace("\\", "/")
        findings: list[Finding] = []
        try:
            fm, keys, body = split_markdown(text)
        except ContractError as exc:
            return [self._finding("fail", "pos_v1_frontmatter_parse", path, str(exc), "Use the restricted pos-v1 YAML dialect.")]

        skill_envelope = (
            isinstance(fm.get("metadata"), dict)
            and fm["metadata"].get("pos_schema_version") == "pos-v1"
        )
        runtime_name = None
        if skill_envelope:
            metadata = fm["metadata"]
            projected_keys = [key.removeprefix("pos_") for key in metadata if key.startswith("pos_")]
            projected = self._project_skill_metadata(fm)
            runtime_name = fm.get("name")
            profile = self.profiles.get(projected.get("type"), {})
            required_runtime = set(profile.get("runtime_required_fields", []))
            optional_runtime = set(profile.get("runtime_optional_fields", []))
            for field in sorted(required_runtime - set(fm)):
                findings.append(self._finding("fail", "pos_v1_skill_runtime_missing_field", path, f"Missing runtime field `{field}`.", "Add the required Skill Runtime field."))
            for field in sorted(set(fm) - required_runtime - optional_runtime):
                findings.append(self._finding("fail", "pos_v1_skill_runtime_unknown_field", path, f"Runtime field `{field}` is not allowed.", "Use only name, description, license, allowed-tools and metadata at top level."))
            if not isinstance(runtime_name, str) or not runtime_name or not SKILL_RUNTIME_NAME_RE.fullmatch(runtime_name) or len(runtime_name) > SKILL_RUNTIME_NAME_MAX:
                findings.append(self._finding("fail", "pos_v1_skill_runtime_name", path, "`name` must be a non-empty lower-kebab runtime key of at most 64 characters.", "Use the skill folder slug as `name`."))
            description = fm.get("description")
            if not isinstance(description, str) or not description.strip() or len(description.strip()) > SKILL_RUNTIME_DESCRIPTION_MAX or any(char in description for char in "<>"):
                findings.append(self._finding("fail", "pos_v1_skill_runtime_description", path, "`description` must be non-empty, at most 1024 characters and contain no angle brackets.", "Write the runtime selection contract directly in `description`."))
            fm = projected
            keys = projected_keys

        if fm.get("schema_version") != "pos-v1":
            return []
        profile_name = fm.get("type")
        if profile_name not in self.profiles:
            return [self._finding("fail", "pos_v1_unknown_profile", path, f"Unknown profile `{profile_name}`.", "Register the profile before using it.")]
        profile = self.profiles[profile_name]
        definitions, required, optional = self.profile_fields(profile_name)
        allowed = required | optional

        if keys[: len(FOUNDATION_ORDER)] != FOUNDATION_ORDER:
            location = "the `metadata` POS namespace" if skill_envelope else "frontmatter"
            findings.append(self._finding("fail", "pos_v1_foundation_order", path, f"Foundation fields must be the first six POS fields in canonical order within {location}.", f"Start the POS record with: {', '.join(FOUNDATION_ORDER)}."))
        missing = sorted(required - set(fm))
        for field in missing:
            findings.append(self._finding("fail", "pos_v1_missing_field", path, f"Missing required field `{field}`.", "Add the field using the registered profile contract."))
        for field in sorted(set(fm) - allowed):
            findings.append(self._finding("fail", "pos_v1_unknown_field", path, f"Field `{field}` is not allowed for profile `{profile_name}`.", "Remove it or admit it centrally through the owning profile/module."))

        for field, value in fm.items():
            definition = definitions.get(field)
            if definition:
                effective = dict(definition)
                constraint = profile.get("module_constraints", {}).get(field, {})
                effective.update(constraint)
                findings.extend(self._validate_field(field, value, effective, path))

        if valid_date(fm.get("created")) and valid_date(fm.get("updated")) and fm["updated"] < fm["created"]:
            findings.append(self._finding("fail", "pos_v1_date_order", path, "`updated` is earlier than `created`.", "Keep `created` immutable and use a non-earlier semantic update date."))

        roots = profile.get("allowed_roots", [])
        if not any(path == root or path.startswith(f"{root}/") for root in roots):
            findings.append(self._finding("fail", "pos_v1_wrong_root", path, f"Profile `{profile_name}` is not allowed at this root.", f"Use one of the allowed roots: {roots}."))
        pattern = profile.get("path_pattern")
        if pattern and not re.fullmatch(pattern, path):
            findings.append(self._finding("fail", "pos_v1_wrong_path", path, f"Path does not match the `{profile_name}` path contract.", f"Use the registered pattern: {pattern}"))
        path_date_field = profile.get("path_date_field")
        path_date = fm.get(path_date_field) if path_date_field else None
        normalized_path_date = None
        if isinstance(path_date, str):
            if valid_date(path_date):
                normalized_path_date = path_date
            elif valid_datetime(path_date):
                normalized_path_date = path_date[:10]
        path_date_prefix_template = profile.get("path_date_prefix_template")
        if normalized_path_date and path_date_prefix_template:
            expected_prefix = path_date_prefix_template.format(
                date=normalized_path_date,
                year=normalized_path_date[:4],
                month=normalized_path_date[5:7],
                day=normalized_path_date[8:10],
            )
            if not path.startswith(expected_prefix):
                findings.append(
                    self._finding(
                        "fail",
                        "pos_v1_path_date_mismatch",
                        path,
                        f"Path year/date does not match `{path_date_field}: {path_date}`.",
                        f"Use a path beginning with `{expected_prefix}`.",
                    )
                )
        path_date_group = profile.get("path_date_group")
        if normalized_path_date and path_date_group and pattern:
            path_match = re.fullmatch(pattern, path)
            if path_match and path_match.group(path_date_group) != normalized_path_date:
                findings.append(
                    self._finding(
                        "fail",
                        "pos_v1_path_date_mismatch",
                        path,
                        f"Path date does not match `{path_date_field}: {path_date}`.",
                        f"Use `{normalized_path_date}` in the `{path_date_group}` path segment.",
                    )
                )
        parent_record = profile.get("parent_record")
        if parent_record and not (parent_record.get("skip_when_relations_disabled") and not resolve_relations):
            parent_match = re.fullmatch(parent_record["when_path_pattern"], path)
            if parent_match:
                required_parent_path = parent_record["required_path_template"].format(**parent_match.groupdict())
                parent_file = self.vault_root / required_parent_path
                if not parent_file.is_file():
                    findings.append(
                        self._finding(
                            "fail",
                            "pos_v1_missing_parent_record",
                            path,
                            f"Required parent record `{required_parent_path}` does not exist.",
                            "Create this artifact only inside an already admitted parent record, or keep it with its domain owner.",
                        )
                    )
                else:
                    try:
                        parent_fm, _, _ = split_markdown(parent_file.read_text(encoding="utf-8"))
                    except ContractError:
                        parent_fm = {}
                    parent_fm = self._project_skill_metadata(parent_fm)
                    required_parent_profile = parent_record["required_profile"]
                    if parent_fm.get("schema_version") != "pos-v1" or parent_fm.get("type") != required_parent_profile:
                        findings.append(
                            self._finding(
                                "fail",
                                "pos_v1_wrong_parent_record",
                                path,
                                f"Parent `{required_parent_path}` is not a pos-v1 `{required_parent_profile}` record.",
                                "Use an already admitted parent record with the required Primary Profile.",
                            )
                        )
        if skill_envelope:
            expected_name = Path(path).parent.name
            if runtime_name != expected_name:
                findings.append(self._finding("fail", "pos_v1_skill_name_path_mismatch", path, f"Runtime `name` `{runtime_name}` differs from skill folder `{expected_name}`.", "Use the lower-kebab skill folder slug as `name`."))

        body_shape = FENCED_BLOCK_RE.sub("", body)
        title = fm.get("title")
        h1 = H1_RE.search(body_shape)
        if isinstance(title, str) and (h1 is None or h1.group(1).strip() != title):
            findings.append(self._finding("fail", "pos_v1_title_h1_mismatch", path, "Body H1 does not exactly match `title`.", "Use exactly one matching H1 after frontmatter."))

        headings = H2_RE.findall(body_shape)
        positions = []
        for section in profile.get("required_sections", []):
            if section not in headings:
                findings.append(self._finding("fail", "pos_v1_missing_section", path, f"Missing required section `## {section}`.", "Add the section using the registered profile template."))
            else:
                positions.append((section, headings.index(section)))
        if positions != sorted(positions, key=lambda item: item[1]):
            findings.append(self._finding("fail", "pos_v1_section_order", path, "Required sections are not in canonical order.", f"Use this order: {profile.get('section_order', [])}."))

        for name, rule in profile.get("conditional_rules", {}).items():
            applies = False
            if rule.get("when_present"):
                applies = rule["when_present"] in fm
            elif rule.get("when_field"):
                applies = fm.get(rule.get("when_field")) in rule.get("when_in", [])
            if applies:
                for field in rule.get("require_fields", []):
                    if field not in fm:
                        findings.append(self._finding("fail", "pos_v1_conditional_field", path, f"Rule `{name}` requires `{field}`.", "Add the required terminal-state evidence field."))
                for field in rule.get("forbid_fields", []):
                    if field in fm:
                        findings.append(
                            self._finding(
                                "fail",
                                "pos_v1_conditional_forbidden_field",
                                path,
                                f"Rule `{name}` forbids `{field}`.",
                                "Remove the field because it contradicts the current lifecycle or outcome.",
                            )
                        )

        if resolve_relations:
            for field, value in fm.items():
                definition = definitions.get(field, {})
                if definition.get("datatype") not in {"wikilink", "wikilink-list"}:
                    continue
                values = value if isinstance(value, list) else [value]
                for link in values:
                    if not isinstance(link, str) or not WIKILINK_RE.fullmatch(link):
                        continue
                    target_key = target_from_wikilink(link)
                    source_key = path[:-3] if path.endswith(".md") else path
                    if definition.get("forbid_self") and target_key.removesuffix(".md") == source_key:
                        findings.append(
                            self._finding(
                                "fail",
                                "pos_v1_self_relation",
                                path,
                                f"`{field}` must not point to the record itself.",
                                "Point to the distinct canonical owner or surviving Idea record.",
                            )
                        )
                        continue
                    target_path, target_fm = self.resolve_link(link)
                    if target_path is None:
                        findings.append(self._finding("fail", "pos_v1_unresolved_relation", path, f"`{field}` target `{link}` cannot be resolved.", "Create or correct the canonical target before writing the relation."))
                        continue
                    expected = definition.get("target_profiles", [])
                    target_type = target_fm.get("type") if target_fm else None
                    target_schema = target_fm.get("schema_version") if target_fm else None
                    if target_schema != "pos-v1":
                        policy = definition.get("legacy_targets", "reject")
                        level = "warn" if policy == "warn" else "fail"
                        findings.append(self._finding(level, "pos_v1_legacy_relation_target", path, f"`{field}` points to non-pos-v1 target `{link}`; target profile and stable ID are not fully verified.", "Migrate the target or retain this explicit pilot warning until its migration wave."))
                    elif expected and target_type not in expected:
                        findings.append(self._finding("fail", "pos_v1_wrong_relation_target", path, f"`{field}` targets profile `{target_type}`, expected one of {expected}.", "Point to a record with an allowed Primary Profile."))
        return findings

    def validate_file(self, path: Path, *, check_duplicate_ids: bool = True) -> list[Finding]:
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(self.vault_root).as_posix()
        except ValueError:
            relative = path.as_posix()
        findings = self.validate_text(resolved.read_text(encoding="utf-8"), relative)
        if check_duplicate_ids:
            try:
                fm, _, _ = split_markdown(resolved.read_text(encoding="utf-8"))
            except ContractError:
                return findings
            fm = self._project_skill_metadata(fm)
            record_id = fm.get("id")
            if fm.get("schema_version") == "pos-v1" and record_id:
                matches = []
                for candidate in self.vault_root.rglob("*.md"):
                    if candidate == resolved or any(part in {".git", ".obsidian", "node_modules"} for part in candidate.parts):
                        continue
                    raw = candidate.read_text(encoding="utf-8", errors="replace")
                    if f"\nid: {record_id}\n" in raw or f'\nid: "{record_id}"\n' in raw:
                        matches.append(candidate.relative_to(self.vault_root).as_posix())
                if matches:
                    findings.append(self._finding("fail", "pos_v1_duplicate_id", relative, f"ID `{record_id}` also occurs in {matches}.", "Assign a fresh UUIDv7 to the newly created duplicate; never change the established record ID."))
        return findings

    def render(self, profile_name: str, title: str, values: dict[str, str]) -> str:
        if profile_name not in self.profiles:
            raise ContractError(f"Unknown profile `{profile_name}`.")
        if profile_name not in self.writable_profiles():
            state = self.registry.get("profile_states", {}).get(profile_name)
            raise ContractError(f"Profile `{profile_name}` is `{state}` and not enabled for new writes.")
        template_path = self.vault_root / self.profiles[profile_name]["template"]
        wrapper = template_path.read_text(encoding="utf-8")
        match = re.search(r"```markdown\n(.*?)\n```", wrapper, re.S)
        if not match:
            raise ContractError(f"Template `{template_path}` has no markdown template fence.")
        rendered = match.group(1)
        replacements = {
            "schema_version": "pos-v1",
            "id": uuid7(),
            "type": profile_name,
            "title": title,
            "date": local_date(self.vault_root).isoformat(),
            **values,
        }
        for key, value in replacements.items():
            rendered = rendered.replace(f"<{key}>", value)
        unresolved = sorted(set(re.findall(r"<([a-z0-9_-]+)>", rendered)))
        if unresolved:
            raise ContractError(f"Missing template values: {unresolved}")
        return rendered + "\n"

    def json_schema_for_profile(self, profile_name: str) -> dict:
        profile = self.profiles[profile_name]
        definitions, required, optional = self.profile_fields(profile_name)
        properties = {}
        for field in self.foundation["field_order"] + sorted((required | optional) - set(self.foundation["field_order"])):
            definition = dict(definitions[field])
            definition.update(profile.get("module_constraints", {}).get(field, {}))
            datatype = definition.get("datatype")
            schema: dict = {}
            if datatype == "literal":
                schema = {"const": definition.get("value")}
            elif datatype == "uuidv7":
                schema = {
                    "type": "string",
                    "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
                }
            elif datatype == "profile-key":
                if field == "type":
                    schema = {"const": profile_name}
                elif definition.get("registered_profile"):
                    schema = {"type": "string", "enum": sorted(self.profiles)}
                else:
                    schema = {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"}
            elif datatype == "lower-kebab":
                schema = {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"}
            elif datatype == "profile-key-list":
                item_schema = {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"}
                if definition.get("registered_profile"):
                    item_schema = {"type": "string", "enum": sorted(self.profiles)}
                schema = {
                    "type": "array",
                    "minItems": int(definition.get("min_items", 1)),
                    "items": item_schema,
                    "uniqueItems": True,
                }
            elif datatype == "plain-text":
                schema = {"type": "string", "minLength": int(definition.get("min_length", 1)), "pattern": "^[^\\n]+$"}
                if definition.get("iana_timezone"):
                    schema["pattern"] = "^[A-Za-z0-9_+.-]+(?:/[A-Za-z0-9_+.-]+)*$"
                elif definition.get("pattern"):
                    schema["pattern"] = definition["pattern"]
            elif datatype == "plain-text-list":
                schema = {
                    "type": "array",
                    "minItems": int(definition.get("min_items", 1)),
                    "items": {"type": "string", "minLength": 1, "pattern": "^[^\\n]+$"},
                    "uniqueItems": True,
                }
            elif datatype == "integer":
                schema = {"type": "integer"}
                if definition.get("minimum") is not None:
                    schema["minimum"] = int(definition["minimum"])
                if definition.get("maximum") is not None:
                    schema["maximum"] = int(definition["maximum"])
            elif datatype == "decimal":
                schema = {"type": "string", "pattern": "^-?(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?$"}
            elif datatype == "date":
                schema = {"type": "string", "format": "date"}
            elif datatype == "datetime":
                schema = {"type": "string", "format": "date-time"}
            elif datatype == "semver":
                schema = {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+(?:-[0-9A-Za-z.-]+)?$"}
            elif datatype == "boolean":
                schema = {"type": "boolean"}
            elif datatype == "enum":
                schema = {"type": "string", "enum": definition.get("enum", [])}
            elif datatype == "uri":
                schema = {"type": "string", "format": "uri"}
            elif datatype == "wikilink":
                schema = {"type": "string", "pattern": "^\\[\\[[^\\]\\n]+\\]\\]$"}
            elif datatype == "wikilink-list":
                schema = {
                    "type": "array",
                    "minItems": int(definition.get("min_items", 1)),
                    "items": {"type": "string", "pattern": "^\\[\\[[^\\]\\n]+\\]\\]$"},
                    "uniqueItems": True,
                }
            else:
                raise ContractError(f"Cannot generate JSON Schema for datatype `{datatype}` on `{field}`.")
            properties[field] = schema

        all_of = []
        for rule in profile.get("conditional_rules", {}).values():
            then_clause: dict = {}
            if rule.get("require_fields"):
                then_clause["required"] = rule.get("require_fields", [])
            if rule.get("forbid_fields"):
                then_clause["allOf"] = [
                    {"not": {"required": [field]}}
                    for field in rule.get("forbid_fields", [])
                ]
            if rule.get("when_present"):
                all_of.append(
                    {
                        "if": {"required": [rule["when_present"]]},
                        "then": then_clause,
                    }
                )
            else:
                all_of.append(
                    {
                        "if": {"properties": {rule["when_field"]: {"enum": rule.get("when_in", [])}}, "required": [rule["when_field"]]},
                        "then": then_clause,
                    }
                )

        if profile.get("frontmatter_layout") == "skill-runtime-envelope":
            prefix = profile.get("metadata_prefix", "pos_")
            metadata_properties = {f"{prefix}{field}": value for field, value in properties.items()}
            metadata_required = [f"{prefix}{field}" for field in self.foundation["field_order"] + sorted(required - set(self.foundation["field_order"]))]
            metadata_schema = {
                "type": "object",
                "additionalProperties": False,
                "properties": metadata_properties,
                "patternProperties": {f"^(?!{re.escape(prefix)}).+$": {}},
                "required": metadata_required,
            }
            if all_of:
                metadata_schema["allOf"] = [
                    {
                        "if": {
                            **({"required": [f"{prefix}{rule['when_present']}"]} if rule.get("when_present") else {
                                "properties": {f"{prefix}{rule['when_field']}": {"enum": rule.get("when_in", [])}},
                                "required": [f"{prefix}{rule['when_field']}"],
                            })
                        },
                        "then": {
                            **(
                                {"required": [f"{prefix}{field}" for field in rule.get("require_fields", [])]}
                                if rule.get("require_fields")
                                else {}
                            ),
                            **(
                                {
                                    "allOf": [
                                        {"not": {"required": [f"{prefix}{field}"]}}
                                        for field in rule.get("forbid_fields", [])
                                    ]
                                }
                                if rule.get("forbid_fields")
                                else {}
                            ),
                        },
                    }
                    for rule in profile.get("conditional_rules", {}).values()
                ]
            return {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": f"https://personal-os.local/schemas/pos-v1/{profile_name}.frontmatter.schema.json",
                "title": f"PersonalOS pos-v1 {profile_name} SKILL.md frontmatter",
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$", "maxLength": SKILL_RUNTIME_NAME_MAX},
                    "description": {"type": "string", "minLength": 1, "maxLength": SKILL_RUNTIME_DESCRIPTION_MAX, "pattern": "^[^<>]+$"},
                    "license": {"type": "string", "minLength": 1},
                    "allowed-tools": {"type": "string", "minLength": 1},
                    "metadata": metadata_schema,
                },
                "required": profile.get("runtime_required_fields", ["name", "description", "metadata"]),
            }
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"https://personal-os.local/schemas/pos-v1/{profile_name}.frontmatter.schema.json",
            "title": f"PersonalOS pos-v1 {profile_name} frontmatter",
            "type": "object",
            "additionalProperties": False,
            "properties": properties,
            "required": self.foundation["field_order"] + sorted(required - set(self.foundation["field_order"])),
        }
        if all_of:
            schema["allOf"] = all_of
        return schema

    def generated_payloads(self) -> dict[Path, str]:
        generated_root = self.model_root / self.registry["generated_root"]
        source_paths = [
            self.model_root / "registry.yaml",
            self.model_root / self.registry["foundation"],
            self.model_root / self.registry["governance"],
            self.model_root / self.registry["deprecations"],
            *[self.model_root / path for path in self.registry["page_shapes"].values()],
            *[self.model_root / path for path in self.registry["modules"].values()],
            *[self.model_root / path for path in self.registry["profiles"].values()],
        ]
        digest = hashlib.sha256()
        for path in sorted(source_paths):
            digest.update(path.relative_to(self.model_root).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
        field_index = {
            "derived": True,
            "contract": self.registry["contract"],
            "registry_version": self.registry["registry_version"],
            "fields": {
                name: {"owner": self.field_owners[name], **self.field_definitions[name]}
                for name in sorted(self.field_owners)
            },
        }
        profile_index = {
            "derived": True,
            "contract": self.registry["contract"],
            "registry_version": self.registry["registry_version"],
            "writable_profiles": self.writable_profiles(),
            "profiles": {
                name: {
                    "write_state": self.registry["profile_states"][name],
                    "page_shape": profile["page_shape"],
                    "canonical_owner": profile["canonical_owner"],
                    "allowed_roots": profile["allowed_roots"],
                    "required_modules": profile.get("required_modules", []),
                    "optional_modules": profile.get("optional_modules", []),
                    "required_fields": self.foundation["field_order"] + profile.get("required_fields", []),
                    "optional_fields": profile.get("optional_fields", []),
                    "required_sections": profile.get("required_sections", []),
                    "template": profile["template"],
                }
                for name, profile in sorted(self.profiles.items())
            },
        }
        manifest = {
            "derived": True,
            "contract": self.registry["contract"],
            "registry_version": self.registry["registry_version"],
            "governance_version": self.governance["governance_version"],
            "source_fingerprint": f"sha256:{digest.hexdigest()}",
            "artifacts": [
                "field-index.json",
                "profile-index.json",
                *[f"schemas/{name}.frontmatter.schema.json" for name in sorted(self.profiles)],
            ],
        }

        def encode(payload: dict) -> str:
            return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

        outputs = {
            generated_root / "manifest.json": encode(manifest),
            generated_root / "field-index.json": encode(field_index),
            generated_root / "profile-index.json": encode(profile_index),
        }
        for profile_name in sorted(self.profiles):
            outputs[generated_root / "schemas" / f"{profile_name}.frontmatter.schema.json"] = encode(
                self.json_schema_for_profile(profile_name)
            )
        return outputs

    def build_generated(self, *, check: bool = False) -> list[str]:
        drift = []
        for path, expected in self.generated_payloads().items():
            actual = path.read_text(encoding="utf-8") if path.is_file() else None
            if actual != expected:
                drift.append(path.relative_to(self.vault_root).as_posix())
                if not check:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(expected, encoding="utf-8")
        return drift


def find_vault_root(start: Path | None = None) -> Path:
    candidate = (start or Path.cwd()).resolve()
    for parent in [candidate, *candidate.parents]:
        if (parent / "system" / "data-model" / "registry.yaml").is_file():
            return parent
    raise ContractError("Could not find PersonalOS root containing system/data-model/registry.yaml.")


def parse_fields(items: list[str]) -> dict[str, str]:
    values = {}
    for item in items:
        if "=" not in item:
            raise ContractError(f"Field assignment must be key=value: `{item}`")
        key, value = item.split("=", 1)
        values[key] = value
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description="PersonalOS pos-v1 registry runtime")
    parser.add_argument("--root", type=Path, default=None)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("new-id")
    sub.add_parser("check-registry")
    build = sub.add_parser("build")
    build.add_argument("--check", action="store_true")
    validate = sub.add_parser("validate")
    validate.add_argument("--files", nargs="+", required=True)
    validate.add_argument("--json", action="store_true")
    render = sub.add_parser("render")
    render.add_argument("--type", required=True)
    render.add_argument("--title", required=True)
    render.add_argument("--field", action="append", default=[])
    args = parser.parse_args()

    if args.command == "new-id":
        print(uuid7())
        return 0
    root = find_vault_root(args.root)
    try:
        contract = Contract(root)
    except ContractError as exc:
        print(f"pos-v1 registry: fail: {exc}", file=sys.stderr)
        return 1
    if args.command == "check-registry":
        print(f"pos-v1 registry: pass ({len(contract.profiles)} profiles, {len(contract.modules)} modules, {len(contract.field_owners)} fields)")
        return 0
    if args.command == "build":
        drift = contract.build_generated(check=args.check)
        if args.check and drift:
            print(f"pos-v1 generated: fail ({len(drift)} drifted artifact(s)): {', '.join(drift)}")
            return 1
        action = "updated" if drift else "current"
        print(f"pos-v1 generated: pass ({len(contract.generated_payloads())} artifact(s), {action})")
        return 0
    if args.command == "render":
        try:
            print(contract.render(args.type, args.title, parse_fields(args.field)), end="")
        except ContractError as exc:
            print(f"pos-v1 render: fail: {exc}", file=sys.stderr)
            return 1
        return 0

    findings: list[Finding] = []
    checked = []
    for raw_path in args.files:
        path = Path(raw_path)
        path = path if path.is_absolute() else root / path
        checked.append(path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix())
        findings.extend(contract.validate_file(path))
    status = "fail" if any(item.level == "fail" for item in findings) else "warn" if findings else "pass"
    payload = {"status": status, "checked_files": checked, "finding_count": len(findings), "findings": [asdict(item) for item in findings]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"pos-v1: {status} ({len(checked)} file(s), {len(findings)} finding(s))")
        for item in findings:
            print(f"[{item.level}] {item.code} {item.path}: {item.message}")
            print(f"      fix: {item.remediation}")
    return 1 if status == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
