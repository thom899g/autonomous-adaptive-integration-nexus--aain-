"""
AAIN Configuration Module
Centralized configuration management for the Autonomous Adaptive Integration Nexus
"""
import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('aain_system.log')
    ]
)
logger = logging.getLogger(__name__)

class IntegrationStatus(Enum):
    """Status enumeration for integration points"""
    ACTIVE = "active"
    PENDING = "pending"
    DEGRADED = "degraded"
    FAILED = "failed"
    OPTIMIZING = "optimizing"
    MAINTENANCE = "maintenance"

class ModuleType(Enum):
    """Types of modules in the ecosystem"""
    DATA_PROCESSOR = "data_processor"
    API_GATEWAY = "api_gateway"
    ML_MODEL = "ml_model"
    DATABASE = "database"
    WORKFLOW_ENGINE = "workflow_engine"
    CUSTOM = "custom"

@dataclass
class AAINConfig:
    """Main configuration data class"""
    # Firestore configuration
    firestore_project_id: str = os.getenv('FIRESTORE_PROJECT_ID', 'evolution-ecosystem')
    firestore_collection: str = "aain_integrations"
    
    # RL Configuration
    rl_learning_rate: float = 0.001
    rl_discount_factor: float = 0.95
    rl_exploration_rate: float = 0.1
    rl_batch_size: int = 32
    rl_memory_capacity: int = 10000
    
    # Monitoring Configuration
    health_check_interval: int = 30  # seconds
    metrics_aggregation_window: int = 300  # seconds
    performance_threshold: float = 0.8  # 80% performance threshold
    
    # Optimization Configuration
    max_connection_pool: int = 100
    min_throughput: float = 100.0  # requests per second
    max_latency: float = 2.0  # seconds
    
    # ML Configuration
    ml_model_path: str = "models/integration_predictor.pkl"
    retrain_interval: int = 86400  # 24 hours in seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AAINConfig':
        """Create config from dictionary"""
        return cls(**data)

class ConfigManager:
    """Configuration manager with validation"""
    
    def __init__(self):
        self.config = AAINConfig()
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate configuration parameters"""
        if self.config.rl_learning_rate <= 0 or self.config.rl_learning_rate > 1:
            raise ValueError("RL learning rate must be between 0 and 1")
        
        if self.config.rl_discount_factor <= 0 or self.config.rl_discount_factor > 1:
            raise ValueError("RL discount factor must be between 0 and 1")
        
        if self.config.performance_threshold <= 0 or self.config.performance_threshold > 1:
            raise ValueError("Performance threshold must be between 0 and 1")
        
        logger.info("Configuration validation passed")
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update configuration with validation"""
        for key, value in updates.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            else:
                logger.warning(f"Ignoring unknown config key: {key}")
        
        self._validate_config()
        logger.info(f"Configuration updated: {updates}")

# Global configuration instance
config_manager = ConfigManager()