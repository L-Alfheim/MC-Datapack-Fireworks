# MC-Datapack-Fireworks

A high-performance Python tool designed to orchestrate grand firework displays in **Minecraft: Java Edition (1.20.1+)**. This engine automates the creation of complex datapacks, featuring randomized delay control, custom aesthetic color palettes, and optimized spatial distribution logic.

## ✨ Key Features

* **Customizable Intervals:** Achieve natural show pacing with randomized delays (e.g., 0.7s - 1.2s) using the `schedule` command.
* **Aesthetic Color Palettes:** Includes curated "Low-Brightness" color sets designed for professional recording, reducing visual noise and GPU strain.
* **Smart NBT Serialization:** A handcrafted serializer that generates Minecraft-compliant NBT strings (unquoted keys) and supports `IntArray` ([I;]) for firework colors.
* **Spatial Logic:** Supports coordinate pools or random distribution within a defined square boundary (e.g., 100x100 area).
* **Datapack Automation:** Automatically generates the entire folder structure, `pack.mcmeta`, and nested `.mcfunction` files.

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* Minecraft: Java Edition 1.20.1 or higher

### Installation

1. Clone the repository:
```bash
git clone https://github.com/L-Alfheim/MC-Datapack-Fireworks.git

```


2. Open `main.py` and configure your square boundary coordinates:
```python
V1 = (x1, y, z1)
V2 = (x2, y, z2)
# ...

```



### Usage

1. Run the script to generate the datapack:
```bash
python main.py

```


2. Copy the generated folder `grand_firework_show` into your Minecraft world's `datapacks` folder.
3. In-game, type `/reload` and then start the show:
```mcfunction
/function grand_firework_show:start

```



## 🛠 Configuration

You can easily adjust the following parameters in the script:

* `total_waves`: Total number of firework bursts.
* `interval_ticks`: The delay between waves (in ticks).
* `num_rockets`: Number of fireworks launched per wave.
* `festival_colors`: Main explosion colors (Decimal RGB).
* `fade_colors`: Fade-out/Trail colors.
