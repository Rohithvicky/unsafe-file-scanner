#!/usr/bin/env python3
"""
Advanced Rule Engine for Unsafe File Scanner
Provides customizable rule sets for security scanning
"""

import os
import re
import fnmatch
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class RuleType(Enum):
    """Types of rules that can be defined."""
    PERMISSION = "permission"
    PATH_PATTERN = "path_pattern"
    FILE_EXTENSION = "file_extension"
    FILE_SIZE = "file_size"
    OWNER_GROUP = "owner_group"
    CUSTOM = "custom"


class RiskLevel(Enum):
    """Risk levels for rules."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class SecurityRule:
    """Represents a security rule."""
    id: str
    name: str
    description: str
    rule_type: RuleType
    pattern: str
    risk_level: RiskLevel
    enabled: bool = True
    custom_function: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RuleMatch:
    """Represents a rule match result."""
    rule_id: str
    rule_name: str
    file_path: str
    risk_level: RiskLevel
    message: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class RuleEngine:
    """Advanced rule engine for security scanning."""
    
    def __init__(self, rules_file: Optional[str] = None):
        self.rules: List[SecurityRule] = []
        self.custom_functions: Dict[str, Callable] = {}
        self.logger = logging.getLogger(__name__)
        
        # Load default rules
        self._load_default_rules()
        
        # Load custom rules if file provided
        if rules_file and os.path.exists(rules_file):
            self.load_rules_from_file(rules_file)
    
    def _load_default_rules(self):
        """Load default security rules."""
        default_rules = [
            # SUID/SGID rules
            SecurityRule(
                id="suid_executable",
                name="SUID Executable",
                description="Files with SUID bit set",
                rule_type=RuleType.PERMISSION,
                pattern="suid",
                risk_level=RiskLevel.HIGH
            ),
            SecurityRule(
                id="sgid_executable",
                name="SGID Executable", 
                description="Files with SGID bit set",
                rule_type=RuleType.PERMISSION,
                pattern="sgid",
                risk_level=RiskLevel.HIGH
            ),
            
            # World-writable rules
            SecurityRule(
                id="world_writable",
                name="World Writable File",
                description="Files writable by all users",
                rule_type=RuleType.PERMISSION,
                pattern="world_writable",
                risk_level=RiskLevel.HIGH
            ),
            SecurityRule(
                id="world_writable_sensitive",
                name="World Writable Sensitive File",
                description="Sensitive files that are world-writable",
                rule_type=RuleType.PATH_PATTERN,
                pattern="**/passwd*,**/shadow*,**/hosts*,**/ssh/**",
                risk_level=RiskLevel.CRITICAL
            ),
            
            # Permission anomalies
            SecurityRule(
                id="executable_not_readable",
                name="Executable Not Readable",
                description="Executable files that are not readable by owner",
                rule_type=RuleType.PERMISSION,
                pattern="executable_not_readable",
                risk_level=RiskLevel.MEDIUM
            ),
            SecurityRule(
                id="directory_no_execute",
                name="Directory Without Execute Permission",
                description="Directories without execute permission for owner",
                rule_type=RuleType.PERMISSION,
                pattern="directory_no_execute",
                risk_level=RiskLevel.MEDIUM
            ),
            
            # Path-based rules
            SecurityRule(
                id="temp_world_writable",
                name="Temporary World Writable",
                description="World-writable files in temporary directories",
                rule_type=RuleType.PATH_PATTERN,
                pattern="**/tmp/**,**/temp/**,**/var/tmp/**",
                risk_level=RiskLevel.LOW
            ),
            SecurityRule(
                id="home_world_writable",
                name="Home Directory World Writable",
                description="World-writable files in home directories",
                rule_type=RuleType.PATH_PATTERN,
                pattern="**/home/**",
                risk_level=RiskLevel.MEDIUM
            ),
            
            # File extension rules
            SecurityRule(
                id="script_world_writable",
                name="Script World Writable",
                description="Executable scripts that are world-writable",
                rule_type=RuleType.FILE_EXTENSION,
                pattern="*.sh,*.py,*.pl,*.rb,*.js,*.php",
                risk_level=RiskLevel.HIGH
            ),
            SecurityRule(
                id="config_world_writable",
                name="Config World Writable",
                description="Configuration files that are world-writable",
                rule_type=RuleType.FILE_EXTENSION,
                pattern="*.conf,*.cfg,*.ini,*.yaml,*.yml,*.json,*.xml",
                risk_level=RiskLevel.HIGH
            ),
            
            # File size rules
            SecurityRule(
                id="large_world_writable",
                name="Large World Writable File",
                description="Large files that are world-writable",
                rule_type=RuleType.FILE_SIZE,
                pattern=">10MB",
                risk_level=RiskLevel.MEDIUM
            ),
            
            # Owner/Group rules
            SecurityRule(
                id="root_owned_world_writable",
                name="Root Owned World Writable",
                description="Root-owned files that are world-writable",
                rule_type=RuleType.OWNER_GROUP,
                pattern="root:*",
                risk_level=RiskLevel.CRITICAL
            ),
        ]
        
        self.rules.extend(default_rules)
    
    def add_rule(self, rule: SecurityRule) -> None:
        """Add a custom rule."""
        self.rules.append(rule)
        self.logger.info(f"Added rule: {rule.name}")
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule by ID."""
        for i, rule in enumerate(self.rules):
            if rule.id == rule_id:
                del self.rules[i]
                self.logger.info(f"Removed rule: {rule.name}")
                return True
        return False
    
    def enable_rule(self, rule_id: str) -> bool:
        """Enable a rule by ID."""
        for rule in self.rules:
            if rule.id == rule_id:
                rule.enabled = True
                self.logger.info(f"Enabled rule: {rule.name}")
                return True
        return False
    
    def disable_rule(self, rule_id: str) -> bool:
        """Disable a rule by ID."""
        for rule in self.rules:
            if rule.id == rule_id:
                rule.enabled = False
                self.logger.info(f"Disabled rule: {rule.name}")
                return True
        return False
    
    def load_rules_from_file(self, rules_file: str) -> None:
        """Load rules from JSON file."""
        try:
            with open(rules_file, 'r') as f:
                rules_data = json.load(f)
            
            for rule_data in rules_data.get('rules', []):
                rule = SecurityRule(
                    id=rule_data['id'],
                    name=rule_data['name'],
                    description=rule_data['description'],
                    rule_type=RuleType(rule_data['rule_type']),
                    pattern=rule_data['pattern'],
                    risk_level=RiskLevel(rule_data['risk_level']),
                    enabled=rule_data.get('enabled', True),
                    custom_function=rule_data.get('custom_function'),
                    metadata=rule_data.get('metadata', {})
                )
                self.add_rule(rule)
            
            self.logger.info(f"Loaded {len(rules_data.get('rules', []))} rules from {rules_file}")
            
        except Exception as e:
            self.logger.error(f"Error loading rules from {rules_file}: {e}")
    
    def save_rules_to_file(self, rules_file: str) -> None:
        """Save rules to JSON file."""
        try:
            rules_data = {
                'rules': [asdict(rule) for rule in self.rules],
                'metadata': {
                    'version': '1.0',
                    'created': str(Path().cwd()),
                    'total_rules': len(self.rules)
                }
            }
            
            with open(rules_file, 'w') as f:
                json.dump(rules_data, f, indent=2)
            
            self.logger.info(f"Saved {len(self.rules)} rules to {rules_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving rules to {rules_file}: {e}")
    
    def evaluate_file(self, file_path: str, file_info: Dict[str, Any]) -> List[RuleMatch]:
        """Evaluate a file against all enabled rules."""
        matches = []
        
        for rule in self.rules:
            if not rule.enabled:
                continue
                
            try:
                match = self._evaluate_rule(rule, file_path, file_info)
                if match:
                    matches.append(match)
            except Exception as e:
                self.logger.error(f"Error evaluating rule {rule.id}: {e}")
        
        return matches
    
    def _evaluate_rule(self, rule: SecurityRule, file_path: str, file_info: Dict[str, Any]) -> Optional[RuleMatch]:
        """Evaluate a single rule against a file."""
        if rule.rule_type == RuleType.PERMISSION:
            return self._evaluate_permission_rule(rule, file_path, file_info)
        elif rule.rule_type == RuleType.PATH_PATTERN:
            return self._evaluate_path_pattern_rule(rule, file_path, file_info)
        elif rule.rule_type == RuleType.FILE_EXTENSION:
            return self._evaluate_file_extension_rule(rule, file_path, file_info)
        elif rule.rule_type == RuleType.FILE_SIZE:
            return self._evaluate_file_size_rule(rule, file_path, file_info)
        elif rule.rule_type == RuleType.OWNER_GROUP:
            return self._evaluate_owner_group_rule(rule, file_path, file_info)
        elif rule.rule_type == RuleType.CUSTOM:
            return self._evaluate_custom_rule(rule, file_path, file_info)
        
        return None
    
    def _evaluate_permission_rule(self, rule: SecurityRule, file_path: str, file_info: Dict[str, Any]) -> Optional[RuleMatch]:
        """Evaluate permission-based rules."""
        permissions = file_info.get('permissions', '')
        issues = file_info.get('issues', [])
        
        if rule.pattern == 'suid' and 'SUID bit set' in issues:
            return RuleMatch(
                rule_id=rule.id,
                rule_name=rule.name,
                file_path=file_path,
                risk_level=rule.risk_level,
                message=f"SUID bit set: {permissions}",
                metadata={'permissions': permissions}
            )
        elif rule.pattern == 'sgid' and 'SGID bit set' in issues:
            return RuleMatch(
                rule_id=rule.id,
                rule_name=rule.name,
                file_path=file_path,
                risk_level=rule.risk_level,
                message=f"SGID bit set: {permissions}",
                metadata={'permissions': permissions}
            )
        elif rule.pattern == 'world_writable' and ('World-writable' in issues or 'Potentially world-writable' in issues):
            return RuleMatch(
                rule_id=rule.id,
                rule_name=rule.name,
                file_path=file_path,
                risk_level=rule.risk_level,
                message=f"World-writable file: {permissions}",
                metadata={'permissions': permissions}
            )
        elif rule.pattern == 'executable_not_readable' and 'Executable but not readable by owner' in issues:
            return RuleMatch(
                rule_id=rule.id,
                rule_name=rule.name,
                file_path=file_path,
                risk_level=rule.risk_level,
                message=f"Executable but not readable: {permissions}",
                metadata={'permissions': permissions}
            )
        elif rule.pattern == 'directory_no_execute' and 'Directory without execute permission' in issues:
            return RuleMatch(
                rule_id=rule.id,
                rule_name=rule.name,
                file_path=file_path,
                risk_level=rule.risk_level,
                message=f"Directory without execute permission: {permissions}",
                metadata={'permissions': permissions}
            )
        
        return None
    
    def _evaluate_path_pattern_rule(self, rule: SecurityRule, file_path: str, file_info: Dict[str, Any]) -> Optional[RuleMatch]:
        """Evaluate path pattern rules."""
        patterns = [p.strip() for p in rule.pattern.split(',')]
        
        for pattern in patterns:
            if fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(os.path.basename(file_path), pattern):
                # Check if this is a sensitive file that's world-writable
                if 'sensitive' in rule.name.lower() and 'world_writable' in file_info.get('issues', []):
                    return RuleMatch(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        file_path=file_path,
                        risk_level=rule.risk_level,
                        message=f"Sensitive file pattern match: {pattern}",
                        metadata={'pattern': pattern, 'permissions': file_info.get('permissions', '')}
                    )
                elif 'world_writable' not in rule.name.lower():
                    return RuleMatch(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        file_path=file_path,
                        risk_level=rule.risk_level,
                        message=f"Path pattern match: {pattern}",
                        metadata={'pattern': pattern}
                    )
        
        return None
    
    def _evaluate_file_extension_rule(self, rule: SecurityRule, file_path: str, file_info: Dict[str, Any]) -> Optional[RuleMatch]:
        """Evaluate file extension rules."""
        extensions = [ext.strip() for ext in rule.pattern.split(',')]
        file_ext = Path(file_path).suffix.lower()
        
        for ext in extensions:
            if file_ext == ext or fnmatch.fnmatch(file_path, f"*{ext}"):
                # Check if file is world-writable
                if 'world_writable' in file_info.get('issues', []) or 'Potentially world-writable' in file_info.get('issues', []):
                    return RuleMatch(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        file_path=file_path,
                        risk_level=rule.risk_level,
                        message=f"File extension match with world-writable: {ext}",
                        metadata={'extension': ext, 'permissions': file_info.get('permissions', '')}
                    )
        
        return None
    
    def _evaluate_file_size_rule(self, rule: SecurityRule, file_path: str, file_info: Dict[str, Any]) -> Optional[RuleMatch]:
        """Evaluate file size rules."""
        file_size = file_info.get('size', 0)
        
        # Parse size pattern (e.g., ">10MB", "<1KB", "=100B")
        pattern = rule.pattern.strip()
        if pattern.startswith('>'):
            size_str = pattern[1:].strip()
            threshold = self._parse_size(size_str)
            if file_size > threshold and 'world_writable' in file_info.get('issues', []):
                return RuleMatch(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    file_path=file_path,
                    risk_level=rule.risk_level,
                    message=f"Large world-writable file: {self._format_size(file_size)}",
                    metadata={'size': file_size, 'threshold': threshold}
                )
        elif pattern.startswith('<'):
            size_str = pattern[1:].strip()
            threshold = self._parse_size(size_str)
            if file_size < threshold:
                return RuleMatch(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    file_path=file_path,
                    risk_level=rule.risk_level,
                    message=f"Small file: {self._format_size(file_size)}",
                    metadata={'size': file_size, 'threshold': threshold}
                )
        
        return None
    
    def _evaluate_owner_group_rule(self, rule: SecurityRule, file_path: str, file_info: Dict[str, Any]) -> Optional[RuleMatch]:
        """Evaluate owner/group rules."""
        owner = file_info.get('owner', '')
        group = file_info.get('group', '')
        owner_group = f"{owner}:{group}"
        
        patterns = [p.strip() for p in rule.pattern.split(',')]
        
        for pattern in patterns:
            if fnmatch.fnmatch(owner_group, pattern) or fnmatch.fnmatch(owner, pattern):
                if 'world_writable' in file_info.get('issues', []) or 'Potentially world-writable' in file_info.get('issues', []):
                    return RuleMatch(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        file_path=file_path,
                        risk_level=rule.risk_level,
                        message=f"Owner/group match with world-writable: {pattern}",
                        metadata={'owner_group': owner_group, 'pattern': pattern}
                    )
        
        return None
    
    def _evaluate_custom_rule(self, rule: SecurityRule, file_path: str, file_info: Dict[str, Any]) -> Optional[RuleMatch]:
        """Evaluate custom rules."""
        if rule.custom_function and rule.custom_function in self.custom_functions:
            try:
                result = self.custom_functions[rule.custom_function](file_path, file_info)
                if result:
                    return RuleMatch(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        file_path=file_path,
                        risk_level=rule.risk_level,
                        message=f"Custom rule match: {rule.custom_function}",
                        metadata={'custom_function': rule.custom_function}
                    )
            except Exception as e:
                self.logger.error(f"Error in custom function {rule.custom_function}: {e}")
        
        return None
    
    def register_custom_function(self, name: str, function: Callable) -> None:
        """Register a custom function for custom rules."""
        self.custom_functions[name] = function
        self.logger.info(f"Registered custom function: {name}")
    
    def _parse_size(self, size_str: str) -> int:
        """Parse size string to bytes."""
        size_str = size_str.upper().strip()
        
        if size_str.endswith('KB'):
            return int(float(size_str[:-2]) * 1024)
        elif size_str.endswith('MB'):
            return int(float(size_str[:-2]) * 1024 * 1024)
        elif size_str.endswith('GB'):
            return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
        elif size_str.endswith('B'):
            return int(float(size_str[:-1]))
        else:
            return int(float(size_str))
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in bytes to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"
    
    def get_rules_summary(self) -> Dict[str, Any]:
        """Get summary of all rules."""
        enabled_rules = [r for r in self.rules if r.enabled]
        disabled_rules = [r for r in self.rules if not r.enabled]
        
        return {
            'total_rules': len(self.rules),
            'enabled_rules': len(enabled_rules),
            'disabled_rules': len(disabled_rules),
            'rules_by_type': {
                rule_type.value: len([r for r in enabled_rules if r.rule_type == rule_type])
                for rule_type in RuleType
            },
            'rules_by_risk': {
                risk_level.value: len([r for r in enabled_rules if r.risk_level == risk_level])
                for risk_level in RiskLevel
            }
        }
