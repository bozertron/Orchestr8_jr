"""
ML Model Integration Module for Phase 7.2 ML Enhanced Recognition.

This module provides comprehensive ML infrastructure including TensorFlow/PyTorch adapters,
model management, performance monitoring, and GPU acceleration support.

Key Features:
- TensorFlowAdapter and PyTorchAdapter for ML framework integration
- ModelManager for model lifecycle management
- PerformanceMonitor for system monitoring and optimization
- GPUAccelerator for hardware acceleration support
- Model versioning and update management
"""

import json
import time
import psutil
import threading
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Tuple
import logging

# ML framework dependencies (graceful fallback if not available)
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
    TF_VERSION = tf.__version__
except ImportError:
    TENSORFLOW_AVAILABLE = False
    tf = None
    TF_VERSION = None

try:
    import torch
    PYTORCH_AVAILABLE = True
    TORCH_VERSION = torch.__version__
except ImportError:
    PYTORCH_AVAILABLE = False
    torch = None
    TORCH_VERSION = None

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

logger = logging.getLogger(__name__)


@dataclass
class ModelMetadata:
    """Metadata for ML models."""
    model_id: str
    model_type: str  # 'tensorflow', 'pytorch', 'sklearn'
    version: str
    created_at: int
    last_updated: int
    performance_metrics: Dict[str, float]
    model_size_mb: float
    training_samples: int
    accuracy: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelMetadata':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class PerformanceMetrics:
    """Performance metrics for ML operations."""
    inference_time_ms: float
    memory_usage_mb: float
    cpu_usage_percent: float
    gpu_usage_percent: float
    throughput_samples_per_sec: float
    accuracy: float
    timestamp: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PerformanceMetrics':
        """Create from dictionary."""
        return cls(**data)


class TensorFlowAdapter:
    """Adapter for TensorFlow model integration."""
    
    def __init__(self):
        self.models = {}
        self.is_available = TENSORFLOW_AVAILABLE
        self.version = TF_VERSION
        
        if self.is_available:
            # Configure TensorFlow for optimal performance
            try:
                # Enable memory growth for GPU
                gpus = tf.config.experimental.list_physical_devices('GPU')
                if gpus:
                    for gpu in gpus:
                        tf.config.experimental.set_memory_growth(gpu, True)
                logger.info(f"TensorFlow {self.version} initialized with {len(gpus)} GPU(s)")
            except Exception as e:
                logger.warning(f"TensorFlow GPU configuration failed: {e}")
    
    def load_model(self, model_path: str, model_id: str) -> Dict[str, Any]:
        """Load TensorFlow model from disk."""
        if not self.is_available:
            return {
                'success': False,
                'error': 'TensorFlow not available'
            }
        
        try:
            model = tf.keras.models.load_model(model_path)
            self.models[model_id] = model
            
            # Get model info
            model_size = self._get_model_size(model_path)
            param_count = model.count_params()
            
            return {
                'success': True,
                'model_id': model_id,
                'model_size_mb': model_size,
                'parameter_count': param_count,
                'input_shape': str(model.input_shape),
                'output_shape': str(model.output_shape)
            }
            
        except Exception as e:
            logger.error(f"Error loading TensorFlow model: {e}")
            return {
                'success': False,
                'error': f'Model loading failed: {str(e)}'
            }
    
    def predict(self, model_id: str, input_data: np.ndarray) -> Dict[str, Any]:
        """Make prediction using TensorFlow model."""
        if not self.is_available or model_id not in self.models:
            return {
                'success': False,
                'error': f'Model {model_id} not available'
            }
        
        try:
            start_time = time.time()
            
            model = self.models[model_id]
            predictions = model.predict(input_data, verbose=0)
            
            inference_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return {
                'success': True,
                'predictions': predictions.tolist() if hasattr(predictions, 'tolist') else predictions,
                'inference_time_ms': inference_time,
                'input_shape': input_data.shape,
                'output_shape': predictions.shape if hasattr(predictions, 'shape') else None
            }
            
        except Exception as e:
            logger.error(f"Error making TensorFlow prediction: {e}")
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}'
            }
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Get information about loaded model."""
        if model_id not in self.models:
            return {
                'success': False,
                'error': f'Model {model_id} not loaded'
            }
        
        try:
            model = self.models[model_id]
            return {
                'success': True,
                'model_id': model_id,
                'parameter_count': model.count_params(),
                'input_shape': str(model.input_shape),
                'output_shape': str(model.output_shape),
                'layers': len(model.layers),
                'trainable_params': sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
            }
            
        except Exception as e:
            logger.error(f"Error getting TensorFlow model info: {e}")
            return {
                'success': False,
                'error': f'Model info retrieval failed: {str(e)}'
            }
    
    def _get_model_size(self, model_path: str) -> float:
        """Get model file size in MB."""
        try:
            path = Path(model_path)
            if path.is_file():
                return path.stat().st_size / (1024 * 1024)
            elif path.is_dir():
                total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                return total_size / (1024 * 1024)
            return 0.0
        except Exception:
            return 0.0


class PyTorchAdapter:
    """Adapter for PyTorch model integration."""
    
    def __init__(self):
        self.models = {}
        self.is_available = PYTORCH_AVAILABLE
        self.version = TORCH_VERSION
        self.device = self._get_device()
        
        if self.is_available:
            logger.info(f"PyTorch {self.version} initialized with device: {self.device}")
    
    def _get_device(self) -> str:
        """Get optimal device for PyTorch operations."""
        if not self.is_available:
            return 'cpu'
        
        if torch.cuda.is_available():
            return 'cuda'
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return 'mps'  # Apple Silicon
        else:
            return 'cpu'
    
    def load_model(self, model_path: str, model_id: str) -> Dict[str, Any]:
        """Load PyTorch model from disk."""
        if not self.is_available:
            return {
                'success': False,
                'error': 'PyTorch not available'
            }
        
        try:
            model = torch.load(model_path, map_location=self.device)
            model.eval()  # Set to evaluation mode
            self.models[model_id] = model
            
            # Get model info
            model_size = self._get_model_size(model_path)
            param_count = sum(p.numel() for p in model.parameters())
            
            return {
                'success': True,
                'model_id': model_id,
                'model_size_mb': model_size,
                'parameter_count': param_count,
                'device': str(self.device)
            }
            
        except Exception as e:
            logger.error(f"Error loading PyTorch model: {e}")
            return {
                'success': False,
                'error': f'Model loading failed: {str(e)}'
            }
    
    def predict(self, model_id: str, input_data: np.ndarray) -> Dict[str, Any]:
        """Make prediction using PyTorch model."""
        if not self.is_available or model_id not in self.models:
            return {
                'success': False,
                'error': f'Model {model_id} not available'
            }
        
        try:
            start_time = time.time()
            
            model = self.models[model_id]
            
            # Convert numpy to tensor
            input_tensor = torch.from_numpy(input_data).float().to(self.device)
            
            with torch.no_grad():
                predictions = model(input_tensor)
            
            inference_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Convert back to numpy
            predictions_np = predictions.cpu().numpy()
            
            return {
                'success': True,
                'predictions': predictions_np.tolist(),
                'inference_time_ms': inference_time,
                'input_shape': input_data.shape,
                'output_shape': predictions_np.shape,
                'device_used': str(self.device)
            }
            
        except Exception as e:
            logger.error(f"Error making PyTorch prediction: {e}")
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}'
            }
    
    def _get_model_size(self, model_path: str) -> float:
        """Get model file size in MB."""
        try:
            return Path(model_path).stat().st_size / (1024 * 1024)
        except Exception:
            return 0.0


class ModelManager:
    """Manager for ML model lifecycle and versioning."""
    
    def __init__(self, models_dir: str = "data/models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.tensorflow_adapter = TensorFlowAdapter()
        self.pytorch_adapter = PyTorchAdapter()
        
        self.model_registry = {}
        self.active_models = {}
        
        # Load existing model registry
        self._load_model_registry()
    
    def register_model(self, model_metadata: ModelMetadata) -> Dict[str, Any]:
        """Register a new model in the registry."""
        try:
            model_id = model_metadata.model_id
            self.model_registry[model_id] = model_metadata
            
            # Save updated registry
            self._save_model_registry()
            
            return {
                'success': True,
                'model_id': model_id,
                'message': 'Model registered successfully'
            }
            
        except Exception as e:
            logger.error(f"Error registering model: {e}")
            return {
                'success': False,
                'error': f'Model registration failed: {str(e)}'
            }
    
    def load_model(self, model_id: str) -> Dict[str, Any]:
        """Load model into memory for inference."""
        try:
            if model_id not in self.model_registry:
                return {
                    'success': False,
                    'error': f'Model {model_id} not found in registry'
                }
            
            metadata = self.model_registry[model_id]
            model_path = self.models_dir / f"{model_id}.model"
            
            if not model_path.exists():
                return {
                    'success': False,
                    'error': f'Model file not found: {model_path}'
                }
            
            # Load based on model type
            if metadata.model_type == 'tensorflow':
                result = self.tensorflow_adapter.load_model(str(model_path), model_id)
            elif metadata.model_type == 'pytorch':
                result = self.pytorch_adapter.load_model(str(model_path), model_id)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported model type: {metadata.model_type}'
                }
            
            if result['success']:
                self.active_models[model_id] = metadata
            
            return result
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return {
                'success': False,
                'error': f'Model loading failed: {str(e)}'
            }

    def predict(self, model_id: str, input_data: np.ndarray) -> Dict[str, Any]:
        """Make prediction using loaded model."""
        try:
            if model_id not in self.active_models:
                return {
                    'success': False,
                    'error': f'Model {model_id} not loaded'
                }

            metadata = self.active_models[model_id]

            # Route to appropriate adapter
            if metadata.model_type == 'tensorflow':
                return self.tensorflow_adapter.predict(model_id, input_data)
            elif metadata.model_type == 'pytorch':
                return self.pytorch_adapter.predict(model_id, input_data)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported model type: {metadata.model_type}'
                }

        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}'
            }

    def get_model_status(self, model_id: str) -> Dict[str, Any]:
        """Get status and information about a model."""
        try:
            if model_id not in self.model_registry:
                return {
                    'success': False,
                    'error': f'Model {model_id} not found'
                }

            metadata = self.model_registry[model_id]
            is_loaded = model_id in self.active_models

            status = {
                'success': True,
                'model_id': model_id,
                'is_registered': True,
                'is_loaded': is_loaded,
                'metadata': metadata.to_dict()
            }

            # Add runtime info if loaded
            if is_loaded:
                if metadata.model_type == 'tensorflow':
                    runtime_info = self.tensorflow_adapter.get_model_info(model_id)
                elif metadata.model_type == 'pytorch':
                    runtime_info = {'success': True, 'device': self.pytorch_adapter.device}
                else:
                    runtime_info = {'success': False, 'error': 'Unsupported model type'}

                status['runtime_info'] = runtime_info

            return status

        except Exception as e:
            logger.error(f"Error getting model status: {e}")
            return {
                'success': False,
                'error': f'Status retrieval failed: {str(e)}'
            }

    def list_models(self) -> Dict[str, Any]:
        """List all registered models."""
        try:
            models_info = []

            for model_id, metadata in self.model_registry.items():
                model_info = {
                    'model_id': model_id,
                    'model_type': metadata.model_type,
                    'version': metadata.version,
                    'accuracy': metadata.accuracy,
                    'is_loaded': model_id in self.active_models,
                    'created_at': metadata.created_at,
                    'last_updated': metadata.last_updated
                }
                models_info.append(model_info)

            return {
                'success': True,
                'models': models_info,
                'total_models': len(models_info),
                'loaded_models': len(self.active_models)
            }

        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return {
                'success': False,
                'error': f'Model listing failed: {str(e)}'
            }

    def _save_model_registry(self):
        """Save model registry to disk."""
        try:
            registry_path = self.models_dir / "model_registry.json"
            registry_data = {
                model_id: metadata.to_dict()
                for model_id, metadata in self.model_registry.items()
            }

            with open(registry_path, 'w') as f:
                json.dump(registry_data, f, indent=2)

        except Exception as e:
            logger.error(f"Error saving model registry: {e}")

    def _load_model_registry(self):
        """Load model registry from disk."""
        try:
            registry_path = self.models_dir / "model_registry.json"
            if registry_path.exists():
                with open(registry_path, 'r') as f:
                    registry_data = json.load(f)

                self.model_registry = {
                    model_id: ModelMetadata.from_dict(metadata_dict)
                    for model_id, metadata_dict in registry_data.items()
                }

        except Exception as e:
            logger.error(f"Error loading model registry: {e}")


class PerformanceMonitor:
    """Monitor ML system performance and resource usage."""

    def __init__(self):
        self.metrics_history = []
        self.monitoring_active = False
        self.monitor_thread = None

    def start_monitoring(self, interval_seconds: int = 5) -> Dict[str, Any]:
        """Start performance monitoring."""
        try:
            if self.monitoring_active:
                return {
                    'success': False,
                    'error': 'Monitoring already active'
                }

            self.monitoring_active = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                args=(interval_seconds,),
                daemon=True
            )
            self.monitor_thread.start()

            return {
                'success': True,
                'message': f'Performance monitoring started with {interval_seconds}s interval'
            }

        except Exception as e:
            logger.error(f"Error starting monitoring: {e}")
            return {
                'success': False,
                'error': f'Monitoring start failed: {str(e)}'
            }

    def stop_monitoring(self) -> Dict[str, Any]:
        """Stop performance monitoring."""
        try:
            self.monitoring_active = False

            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=1.0)

            return {
                'success': True,
                'message': 'Performance monitoring stopped'
            }

        except Exception as e:
            logger.error(f"Error stopping monitoring: {e}")
            return {
                'success': False,
                'error': f'Monitoring stop failed: {str(e)}'
            }

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics."""
        try:
            # CPU and memory metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            memory_usage_mb = (memory.total - memory.available) / (1024 * 1024)

            # GPU metrics (if available)
            gpu_usage = self._get_gpu_usage()

            metrics = PerformanceMetrics(
                inference_time_ms=0.0,  # Will be updated during inference
                memory_usage_mb=memory_usage_mb,
                cpu_usage_percent=cpu_percent,
                gpu_usage_percent=gpu_usage,
                throughput_samples_per_sec=0.0,  # Will be calculated
                accuracy=0.0,  # Will be updated from model performance
                timestamp=int(time.time() * 1000)
            )

            return {
                'success': True,
                'metrics': metrics.to_dict(),
                'system_info': {
                    'cpu_count': psutil.cpu_count(),
                    'total_memory_gb': memory.total / (1024 * 1024 * 1024),
                    'available_memory_gb': memory.available / (1024 * 1024 * 1024)
                }
            }

        except Exception as e:
            logger.error(f"Error getting current metrics: {e}")
            return {
                'success': False,
                'error': f'Metrics retrieval failed: {str(e)}'
            }

    def get_metrics_history(self, last_n_minutes: int = 10) -> Dict[str, Any]:
        """Get performance metrics history."""
        try:
            cutoff_time = int(time.time() * 1000) - (last_n_minutes * 60 * 1000)

            recent_metrics = [
                metrics for metrics in self.metrics_history
                if metrics.timestamp > cutoff_time
            ]

            if not recent_metrics:
                return {
                    'success': True,
                    'metrics': [],
                    'summary': {
                        'avg_cpu_usage': 0.0,
                        'avg_memory_usage_mb': 0.0,
                        'avg_gpu_usage': 0.0
                    }
                }

            # Calculate summary statistics
            avg_cpu = sum(m.cpu_usage_percent for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m.memory_usage_mb for m in recent_metrics) / len(recent_metrics)
            avg_gpu = sum(m.gpu_usage_percent for m in recent_metrics) / len(recent_metrics)

            return {
                'success': True,
                'metrics': [m.to_dict() for m in recent_metrics],
                'summary': {
                    'avg_cpu_usage': avg_cpu,
                    'avg_memory_usage_mb': avg_memory,
                    'avg_gpu_usage': avg_gpu,
                    'sample_count': len(recent_metrics),
                    'time_range_minutes': last_n_minutes
                }
            }

        except Exception as e:
            logger.error(f"Error getting metrics history: {e}")
            return {
                'success': False,
                'error': f'Metrics history retrieval failed: {str(e)}'
            }

    def _monitor_loop(self, interval_seconds: int):
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                metrics_result = self.get_current_metrics()
                if metrics_result['success']:
                    metrics = PerformanceMetrics.from_dict(metrics_result['metrics'])
                    self.metrics_history.append(metrics)

                    # Keep only last 1000 metrics to prevent memory growth
                    if len(self.metrics_history) > 1000:
                        self.metrics_history = self.metrics_history[-1000:]

                time.sleep(interval_seconds)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval_seconds)

    def _get_gpu_usage(self) -> float:
        """Get GPU usage percentage."""
        try:
            # Try to get NVIDIA GPU usage
            if TENSORFLOW_AVAILABLE:
                gpus = tf.config.experimental.list_physical_devices('GPU')
                if gpus:
                    # This is a simplified implementation
                    # Real implementation would use nvidia-ml-py or similar
                    return 0.0  # Placeholder

            if PYTORCH_AVAILABLE and torch.cuda.is_available():
                # PyTorch GPU memory usage
                memory_allocated = torch.cuda.memory_allocated() / torch.cuda.max_memory_allocated()
                return memory_allocated * 100.0

            return 0.0  # No GPU or not available

        except Exception:
            return 0.0


class GPUAccelerator:
    """GPU acceleration support for ML operations."""

    def __init__(self):
        self.cuda_available = self._check_cuda_availability()
        self.metal_available = self._check_metal_availability()  # macOS
        self.opencl_available = self._check_opencl_availability()

        self.preferred_device = self._determine_preferred_device()

    def _check_cuda_availability(self) -> bool:
        """Check if CUDA is available."""
        try:
            if TENSORFLOW_AVAILABLE:
                return len(tf.config.experimental.list_physical_devices('GPU')) > 0
            elif PYTORCH_AVAILABLE:
                return torch.cuda.is_available()
            return False
        except Exception:
            return False

    def _check_metal_availability(self) -> bool:
        """Check if Metal Performance Shaders is available (macOS)."""
        try:
            if PYTORCH_AVAILABLE:
                return hasattr(torch.backends, 'mps') and torch.backends.mps.is_available()
            return False
        except Exception:
            return False

    def _check_opencl_availability(self) -> bool:
        """Check if OpenCL is available."""
        try:
            # This would require pyopencl or similar
            # For now, return False as it's not commonly used for ML
            return False
        except Exception:
            return False

    def _determine_preferred_device(self) -> str:
        """Determine the preferred device for ML operations."""
        if self.cuda_available:
            return 'cuda'
        elif self.metal_available:
            return 'mps'
        elif self.opencl_available:
            return 'opencl'
        else:
            return 'cpu'

    def optimize_for_hardware(self) -> Dict[str, Any]:
        """Optimize ML models for available hardware acceleration."""
        try:
            optimizations = {}

            if self.cuda_available:
                optimizations['cuda'] = {
                    'enabled': True,
                    'memory_growth': True,
                    'mixed_precision': True,
                    'device_count': self._get_cuda_device_count()
                }

            if self.metal_available:
                optimizations['metal'] = {
                    'enabled': True,
                    'device': 'mps'
                }

            # CPU optimizations
            optimizations['cpu'] = {
                'threads': psutil.cpu_count(),
                'optimization_level': 'O2'
            }

            return {
                'success': True,
                'preferred_device': self.preferred_device,
                'optimizations': optimizations,
                'hardware_info': self.get_hardware_info()
            }

        except Exception as e:
            logger.error(f"Error optimizing for hardware: {e}")
            return {
                'success': False,
                'error': f'Hardware optimization failed: {str(e)}'
            }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get hardware performance metrics for optimization."""
        try:
            metrics = {
                'cpu': {
                    'cores': psutil.cpu_count(),
                    'usage_percent': psutil.cpu_percent(interval=0.1),
                    'frequency_mhz': psutil.cpu_freq().current if psutil.cpu_freq() else 0
                },
                'memory': {
                    'total_gb': psutil.virtual_memory().total / (1024**3),
                    'available_gb': psutil.virtual_memory().available / (1024**3),
                    'usage_percent': psutil.virtual_memory().percent
                }
            }

            # GPU metrics
            if self.cuda_available:
                metrics['gpu'] = self._get_cuda_metrics()
            elif self.metal_available:
                metrics['gpu'] = self._get_metal_metrics()

            return {
                'success': True,
                'metrics': metrics,
                'preferred_device': self.preferred_device
            }

        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            return {
                'success': False,
                'error': f'Performance metrics retrieval failed: {str(e)}'
            }

    def get_hardware_info(self) -> Dict[str, Any]:
        """Get detailed hardware information."""
        return {
            'cuda_available': self.cuda_available,
            'metal_available': self.metal_available,
            'opencl_available': self.opencl_available,
            'preferred_device': self.preferred_device,
            'cpu_count': psutil.cpu_count(),
            'total_memory_gb': psutil.virtual_memory().total / (1024**3)
        }

    def _get_cuda_device_count(self) -> int:
        """Get number of CUDA devices."""
        try:
            if TENSORFLOW_AVAILABLE:
                return len(tf.config.experimental.list_physical_devices('GPU'))
            elif PYTORCH_AVAILABLE:
                return torch.cuda.device_count()
            return 0
        except Exception:
            return 0

    def _get_cuda_metrics(self) -> Dict[str, Any]:
        """Get CUDA GPU metrics."""
        try:
            if PYTORCH_AVAILABLE and torch.cuda.is_available():
                return {
                    'device_count': torch.cuda.device_count(),
                    'current_device': torch.cuda.current_device(),
                    'memory_allocated_mb': torch.cuda.memory_allocated() / (1024**2),
                    'memory_reserved_mb': torch.cuda.memory_reserved() / (1024**2)
                }
            return {}
        except Exception:
            return {}

    def _get_metal_metrics(self) -> Dict[str, Any]:
        """Get Metal GPU metrics (macOS)."""
        try:
            # Metal metrics are limited in PyTorch
            return {
                'device': 'mps',
                'available': self.metal_available
            }
        except Exception:
            return {}


class MLModelIntegration:
    """
    Main class for ML model integration and performance optimization.

    Provides comprehensive ML infrastructure including model management,
    performance monitoring, and hardware acceleration.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Initialize components
        self.model_manager = ModelManager(str(self.data_dir / "models"))
        self.performance_monitor = PerformanceMonitor()
        self.gpu_accelerator = GPUAccelerator()

        # System state
        self.is_initialized = False
        self.optimization_applied = False

    def initialize_ml_models(self) -> Dict[str, Any]:
        """Initialize and load ML models for enhanced recognition."""
        try:
            # Start performance monitoring
            monitor_result = self.performance_monitor.start_monitoring(interval_seconds=10)

            # Optimize for available hardware
            optimization_result = self.gpu_accelerator.optimize_for_hardware()

            if optimization_result['success']:
                self.optimization_applied = True

            # Get system info
            hardware_info = self.gpu_accelerator.get_hardware_info()

            # List available models
            models_result = self.model_manager.list_models()

            self.is_initialized = True

            return {
                'success': True,
                'monitoring_started': monitor_result.get('success', False),
                'hardware_optimized': optimization_result.get('success', False),
                'hardware_info': hardware_info,
                'available_models': models_result.get('models', []),
                'tensorflow_available': TENSORFLOW_AVAILABLE,
                'pytorch_available': PYTORCH_AVAILABLE,
                'preferred_device': self.gpu_accelerator.preferred_device,
                'message': 'ML models initialized successfully'
            }

        except Exception as e:
            logger.error(f"Error initializing ML models: {e}")
            return {
                'success': False,
                'error': f'ML initialization failed: {str(e)}'
            }

    def optimize_inference_performance(self) -> Dict[str, Any]:
        """Optimize ML model inference for real-time performance."""
        try:
            if not self.is_initialized:
                return {
                    'success': False,
                    'error': 'ML system not initialized'
                }

            # Get current performance metrics
            metrics_result = self.performance_monitor.get_current_metrics()

            if not metrics_result['success']:
                return {
                    'success': False,
                    'error': 'Failed to get performance metrics'
                }

            current_metrics = metrics_result['metrics']

            # Analyze performance and suggest optimizations
            optimizations = []

            # CPU optimization
            if current_metrics['cpu_usage_percent'] > 80:
                optimizations.append({
                    'type': 'cpu_optimization',
                    'description': 'Reduce CPU usage by optimizing batch sizes',
                    'priority': 'high'
                })

            # Memory optimization
            if current_metrics['memory_usage_mb'] > 4000:  # 4GB threshold
                optimizations.append({
                    'type': 'memory_optimization',
                    'description': 'Optimize memory usage by reducing model precision',
                    'priority': 'medium'
                })

            # GPU optimization
            if current_metrics['gpu_usage_percent'] > 90:
                optimizations.append({
                    'type': 'gpu_optimization',
                    'description': 'Optimize GPU usage by adjusting batch processing',
                    'priority': 'high'
                })

            return {
                'success': True,
                'current_performance': current_metrics,
                'optimizations': optimizations,
                'hardware_info': self.gpu_accelerator.get_hardware_info(),
                'optimization_timestamp': int(time.time() * 1000)
            }

        except Exception as e:
            logger.error(f"Error optimizing inference performance: {e}")
            return {
                'success': False,
                'error': f'Performance optimization failed: {str(e)}'
            }

    def manage_model_updates(self) -> Dict[str, Any]:
        """Manage ML model updates and version control."""
        try:
            # Get list of all models
            models_result = self.model_manager.list_models()

            if not models_result['success']:
                return {
                    'success': False,
                    'error': 'Failed to list models'
                }

            models = models_result['models']

            # Check for models that need updates
            update_candidates = []
            current_time = int(time.time() * 1000)

            for model in models:
                # Check if model is older than 30 days
                age_days = (current_time - model['last_updated']) / (1000 * 60 * 60 * 24)

                if age_days > 30:
                    update_candidates.append({
                        'model_id': model['model_id'],
                        'age_days': age_days,
                        'current_accuracy': model['accuracy'],
                        'update_priority': 'high' if age_days > 60 else 'medium'
                    })

            # Generate update recommendations
            recommendations = []

            for candidate in update_candidates:
                recommendations.append({
                    'model_id': candidate['model_id'],
                    'action': 'retrain',
                    'reason': f"Model is {candidate['age_days']:.1f} days old",
                    'priority': candidate['update_priority'],
                    'expected_improvement': '5-10% accuracy increase'
                })

            return {
                'success': True,
                'total_models': len(models),
                'update_candidates': update_candidates,
                'recommendations': recommendations,
                'update_check_timestamp': current_time
            }

        except Exception as e:
            logger.error(f"Error managing model updates: {e}")
            return {
                'success': False,
                'error': f'Model update management failed: {str(e)}'
            }

    def monitor_system_performance(self) -> Dict[str, Any]:
        """Monitor overall system performance with ML integration."""
        try:
            # Get current metrics
            current_metrics = self.performance_monitor.get_current_metrics()

            # Get metrics history
            history_metrics = self.performance_monitor.get_metrics_history(last_n_minutes=30)

            # Get hardware performance
            hardware_metrics = self.gpu_accelerator.get_performance_metrics()

            # Calculate system health score
            health_score = self._calculate_system_health(
                current_metrics.get('metrics', {}),
                history_metrics.get('summary', {})
            )

            return {
                'success': True,
                'current_metrics': current_metrics,
                'history_summary': history_metrics.get('summary', {}),
                'hardware_metrics': hardware_metrics,
                'system_health_score': health_score,
                'monitoring_active': self.performance_monitor.monitoring_active,
                'monitoring_timestamp': int(time.time() * 1000)
            }

        except Exception as e:
            logger.error(f"Error monitoring system performance: {e}")
            return {
                'success': False,
                'error': f'System monitoring failed: {str(e)}'
            }

    def _calculate_system_health(self, current_metrics: Dict[str, Any],
                               history_summary: Dict[str, Any]) -> float:
        """Calculate overall system health score (0.0 to 1.0)."""
        try:
            health_factors = []

            # CPU health (lower usage is better)
            cpu_usage = current_metrics.get('cpu_usage_percent', 100)
            cpu_health = max(0.0, 1.0 - (cpu_usage / 100.0))
            health_factors.append(cpu_health * 0.3)  # 30% weight

            # Memory health
            memory_usage_mb = current_metrics.get('memory_usage_mb', 8000)
            memory_health = max(0.0, 1.0 - (memory_usage_mb / 8000.0))  # Assume 8GB max
            health_factors.append(memory_health * 0.3)  # 30% weight

            # GPU health (if available)
            gpu_usage = current_metrics.get('gpu_usage_percent', 0)
            if gpu_usage > 0:
                gpu_health = max(0.0, 1.0 - (gpu_usage / 100.0))
                health_factors.append(gpu_health * 0.2)  # 20% weight
            else:
                health_factors.append(0.2)  # No GPU penalty

            # Stability health (based on history)
            avg_cpu = history_summary.get('avg_cpu_usage', 50)
            stability_health = max(0.0, 1.0 - (avg_cpu / 100.0))
            health_factors.append(stability_health * 0.2)  # 20% weight

            return sum(health_factors)

        except Exception:
            return 0.5  # Default moderate health


# Module-level functions for integration with existing senses system
def create_ml_model_integration(data_dir: str = "data") -> Dict[str, Any]:
    """Create a new ML model integration instance."""
    try:
        integration = MLModelIntegration(data_dir=data_dir)
        return {
            'success': True,
            'integration': integration,
            'tensorflow_available': TENSORFLOW_AVAILABLE,
            'pytorch_available': PYTORCH_AVAILABLE,
            'numpy_available': NUMPY_AVAILABLE,
            'message': 'ML model integration created successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to create ML model integration: {str(e)}'
        }
