# steganography-tool
Steganographic attack &amp; detection tool with AES-256 encryption and C++ acceleration

## Benchmark Results

| Algorithm | Accuracy | Precision | Recall |
|-----------|----------|-----------|--------|
| LSB Analysis | 84% | 83% | 85% |
| Chi-Square | 91% | 90% | 92% |
| RS Analysis | 88% | 87% | 89% |
| Ensemble Detector | 93% | 92% | 94% |

Benchmark dataset:
- 50 clean images
- 50 stego images

## Heatmap Visualization

Original vs Stego vs Heatmap

- Heatmaps amplify hidden LSB modifications
- Used for forensic visualization
- Helps localize suspicious embedding regions