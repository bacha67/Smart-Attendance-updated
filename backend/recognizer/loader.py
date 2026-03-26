import os
import pickle
import numpy as np
from config import config

class ModelLoader:
    def __init__(self):
        self.classifier = None
        self.label_encoder = None
        self.label_classes = None
        self.scaler = None
        self.metadata = {}
        self.model_loaded = False
        
    def load_models(self):
        """Load classifier and label encoder from disk"""
        try:
            model_path = config.MODEL_PATH
            
            print(f"🔍 [Loader] Model directory: {model_path}")
            print(f"🔍 [Loader] Absolute path: {os.path.abspath(model_path)}")
            
            # Check if model directory exists
            if not os.path.exists(model_path):
                print(f"❌ [Loader] Model directory does not exist: {model_path}")
                print(f"💡 [Loader] Create it with: mkdir {model_path}")
                return False
            
            # Define model file paths
            classifier_path = os.path.join(model_path, 'face_classifier_v1.pkl')
            encoder_path = os.path.join(model_path, 'label_encoder.pkl')
            classes_path = os.path.join(model_path, 'label_encoder_classes.npy')
            
            print(f"🔍 [Loader] Looking for classifier: {classifier_path}")
            
            # Check if classifier exists
            if not os.path.exists(classifier_path):
                print(f"❌ [Loader] Classifier not found: {classifier_path}")
                print(f"💡 [Loader] Required file: face_classifier_v1.pkl")
                
                # List files in directory to help debug
                try:
                    files = os.listdir(model_path)
                    print(f"📁 [Loader] Files in {model_path}:")
                    for f in files:
                        if not f.startswith('.'):
                            print(f"   - {f}")
                except Exception as e:
                    print(f"❌ [Loader] Cannot list directory: {e}")
                
                return False
            
            # Load classifier
            print(f"🔍 [Loader] Loading classifier...")
            try:
                with open(classifier_path, 'rb') as f:
                    data = pickle.load(f)
                
                # Check if it's the new format (dict with metadata)
                if isinstance(data, dict) and 'classifier' in data:
                    print(f"✅ [Loader] Detected new model format with metadata")
                    self.classifier = data['classifier']
                    self.scaler = data.get('scaler', None)
                    self.label_encoder = data.get('label_encoder', None)
                    self.metadata = data.get('metadata', {})
                    
                    print(f"✅ [Loader] Classifier type: {type(self.classifier).__name__}")
                    print(f"✅ [Loader] Scaler: {type(self.scaler).__name__ if self.scaler else 'None'}")
                    print(f"✅ [Loader] Embedding dim: {self.metadata.get('embedding_dim', 'unknown')}")
                    print(f"✅ [Loader] Threshold: {self.metadata.get('threshold', 'unknown')}")
                    print(f"✅ [Loader] Num classes: {self.metadata.get('num_classes', 'unknown')}")
                    
                    # Verify classifier is not a dict
                    if isinstance(self.classifier, dict):
                        print(f"❌ [Loader] ERROR: Classifier is still a dict!")
                        print(f"   Keys: {self.classifier.keys()}")
                        return False
                else:
                    # Old format - just the classifier
                    print(f"✅ [Loader] Detected old model format")
                    self.classifier = data
                    self.scaler = None
                    self.metadata = {}
                    print(f"✅ [Loader] Classifier type: {type(self.classifier).__name__}")
                
            except Exception as e:
                print(f"❌ [Loader] Error loading classifier: {e}")
                print(f"💡 [Loader] File may be corrupted or incompatible")
                return False
            
            # Load label encoder
            print(f"🔍 [Loader] Looking for label encoder: {encoder_path}")
            if os.path.exists(encoder_path):
                try:
                    with open(encoder_path, 'rb') as f:
                        self.label_encoder = pickle.load(f)
                    print(f"✅ [Loader] Loaded label encoder from {encoder_path}")
                    print(f"✅ [Loader] Encoder type: {type(self.label_encoder).__name__}")
                except Exception as e:
                    print(f"⚠️  [Loader] Error loading label encoder: {e}")
                    print(f"⚠️  [Loader] Will use class array instead")
            else:
                print(f"⚠️  [Loader] Label encoder not found (will use class array)")
            
            # Load label classes
            print(f"🔍 [Loader] Looking for label classes: {classes_path}")
            if os.path.exists(classes_path):
                try:
                    self.label_classes = np.load(classes_path, allow_pickle=True)
                    print(f"✅ [Loader] Loaded {len(self.label_classes)} classes")
                    print(f"✅ [Loader] Classes: {self.label_classes[:5]}..." if len(self.label_classes) > 5 else f"✅ [Loader] Classes: {self.label_classes}")
                except Exception as e:
                    print(f"⚠️  [Loader] Error loading label classes: {e}")
                    print(f"⚠️  [Loader] Will use numeric labels")
            else:
                print(f"⚠️  [Loader] Label classes not found (will use numeric labels)")
            
            self.model_loaded = True
            print(f"✅ [Loader] All models loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ [Loader] Unexpected error loading models: {e}")
            import traceback
            traceback.print_exc()
            self.model_loaded = False
            return False
    
    def is_loaded(self):
        """Check if models are loaded"""
        return self.model_loaded
    
    def get_classifier(self):
        """Get classifier instance"""
        return self.classifier
    
    def get_label_encoder(self):
        """Get label encoder instance"""
        return self.label_encoder
    
    def get_classes(self):
        """Get label classes"""
        return self.label_classes
    
    def get_scaler(self):
        """Get scaler instance"""
        return self.scaler
    
    def get_metadata(self):
        """Get model metadata"""
        return self.metadata
    
    def get_threshold(self):
        """Get confidence threshold"""
        # Load threshold from model metadata when available, but validate it
        raw = self.metadata.get('threshold', None)
        try:
            if raw is None:
                return float(config.RECOGNITION_CONFIDENCE_THRESHOLD)
            t = float(raw)
        except Exception:
            # Fallback to configured threshold on parse error
            return float(config.RECOGNITION_CONFIDENCE_THRESHOLD)

        # Sanity-check the threshold. Extremely high or low thresholds are likely
        # to be the result of brittle heuristics during training. If the loaded
        # threshold is outside sensible bounds, fall back to the configured value.
        if t < 0.05 or t > 0.95:
            print(f"⚠️ [Loader] Loaded threshold {t:.4f} looks suspicious; using config threshold {config.RECOGNITION_CONFIDENCE_THRESHOLD:.4f} instead")
            return float(config.RECOGNITION_CONFIDENCE_THRESHOLD)

        return t

# Global model loader instance
model_loader = ModelLoader()
