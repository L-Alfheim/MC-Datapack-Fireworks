import random
import os
from typing import List, Dict, Union, Any

class NBTSerializer:
    """NBT 序列化工具类。
    
    负责将 Python 数据结构转换为 Minecraft 无引号 NBT 字符串，
    并自动处理 IntArray ([I;]) 格式。
    """

    @staticmethod
    def serialize(data: Any) -> str:
        """将对象序列化为 Minecraft 兼容的 NBT 文本。"""
        if isinstance(data, dict):
            # 处理字典：键名不加引号
            pairs = [f"{k}:{NBTSerializer.serialize(v)}" for k, v in data.items()]
            return "{" + ",".join(pairs) + "}"
        
        elif isinstance(data, list):
            # 自动识别整数列表并转换为 [I;1,2,3] 格式
            if data and all(isinstance(x, int) for x in data):
                return f"[I;{','.join(map(str, data))}]"
            # 普通列表处理
            return "[" + ",".join(NBTSerializer.serialize(x) for x in data) + "]"
        
        elif isinstance(data, str):
            # 字符串值不加引号
            return data
        
        return str(data)


class FireworkCommandGenerator:
    """烟花指令生成引擎。
    
    包含坐标池管理、节日算法逻辑及 NBT 组装。
    """

    def __init__(self):
        # 您的坐标池：支持 [x, y, z] 或 字符串
        self.coordinate_pool = [
            [-534, 66, -970],
            [-534, 66, -962],
            [-530, 66, -962],
            [-530, 66, -970],
            [-538, 66, -970],
            [-538, 66, -962]
        ]
        
        # # 节日颜色 (RGB 十进制)
        # self.festival_colors = [
        #     11743532, 3887386, 2437522, 8073150, 2651799, 
        #     14188952, 4312372, 14602026, 6719955, 12801229, 15435844
        # ]

        # 红色系、金色、橙色、紫色等喜庆颜色
        self.festival_colors = [
            10496000,   # 深红 (Dark Red)
            12541952,   # 砖橙 (Burnt Orange)
            11833112,   # 柔和金 (Muted Gold)
            13260,      # 深海蓝 (Deep Blue)
            26214,      # 森林绿 (Forest Green)
            10496128,   # 深洋红 (Dark Magenta)
            13391232,   # 藕粉色 (Dusty Pink)
            11842560,   # 芥末黄 (Mustard Yellow)
            6704255,    # 暮紫 (Twilight Purple)
            32896       # 鸭翅青 (Teal)
            11743532, 
            3887386, 
            2437522, 
            8073150, 
            2651799, 
            14188952, 
            4312372, 
            14602026, 
            6719955, 
            12801229, 
            15435844
        ]
        
        # 渐变色（稍微暗一些的颜色，适合做渐变色）
        self.fade_colors = [
            14423100,   # 暗红色 #DC143C
            13789470,   # 深橙色 #D2691E
            13408512,   # 暗金色 #CC9900
            255,        # 深蓝色 #0000FF
            32768,      # 深绿色 #008000
            8388736,    # 深紫色 #800080
            16711884,   # 深粉色 #FF1493
            10079232,   # 暗黄色 #996600
            10289152,   # 深紫色 #9D00FF
            32767,      # 深青色 #007FFF
        ]
        
        # 类型权重: 0-小球, 1-大球, 4-星形
        self.type_weights = {0: 0.5, 1: 0.3, 4: 0.2}
        
        # 飞行配置: (LifeTime, Flight, 权重)
        self.flight_options = [
            (40, 2, 0.2), (50, 3, 0.6), (60, 3, 0.2)
        ]

    def _get_random_coord(self) -> str:
        """从坐标池中随机抽取并格式化坐标。"""
        if not self.coordinate_pool:
            return "~ ~ ~"
        choice = random.choice(self.coordinate_pool)
        return " ".join(map(str, choice)) if isinstance(choice, list) else str(choice)

    def _generate_explosion(self) -> Dict:
        """生成单个爆炸 NBT 字典。"""
        t_ids = list(self.type_weights.keys())
        t_wts = list(self.type_weights.values())
        
        return {
            "Type": random.choices(t_ids, weights=t_wts)[0],
            "Flicker": 1 if random.random() < 0.3 else 0,
            "Trail": 1 if random.random() < 0.3 else 0,
            "Colors": random.sample(self.festival_colors, random.randint(1, 3)),
            "FadeColors": random.sample(self.fade_colors, random.randint(1, 2))
        }

    def generate_command(self, multiple: bool = True) -> str:
        """生成单条完整的 /summon 烟花命令。"""
        coord = self._get_random_coord()
        
        # 选取飞行参数
        f_time, f_level, _ = random.choices(
            self.flight_options, 
            weights=[opt[2] for opt in self.flight_options]
        )[0]
        
        # 计算爆炸逻辑
        num_exp = random.randint(2, 4) if multiple and random.random() < 0.2 else 1
        explosions = [self._generate_explosion() for _ in range(num_exp)]
        
        # 组装结构
        data = {
            "LifeTime": f_time,
            "FireworksItem": {
                "id": "firework_rocket",
                "Count": 1,
                "tag": {
                    "Fireworks": {
                        "Explosions": explosions,
                        "Flight": f_level
                    }
                }
            }
        }
        
        return f"/summon firework_rocket {coord} {NBTSerializer.serialize(data)}"

    def batch_generate(self, count: int = 10) -> List[str]:
        """批量生成指令列表。"""
        return [self.generate_command() for _ in range(count)]
    

    # --- 这里的代码才是“开关” ---
if __name__ == "__main__":
    # 1. 实例化生成器
    generator = FireworkCommandGenerator()
    
    # 2. 生成一个命令
    cmd = generator.generate_command()
    
    # 3. 打印到控制台，这样你才能看到东西
    print("生成的命令如下：")
    print(cmd)
    
    # 4. 如果你想生成一堆并保存到文件
    print("\n正在生成 10 条命令并保存到 fireworks.txt...")
    commands = generator.batch_generate(10)
    with open("fireworks.txt", "w", encoding="utf-8") as f:
        for c in commands:
            f.write(c + "\n")
    print("保存成功！")
    # 在保存文件后添加这行
file_path = os.path.abspath("fireworks.txt")
print(f"文件已保存在绝对路径: {file_path}")