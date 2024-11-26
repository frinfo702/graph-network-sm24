import random

import matplotlib.pyplot as plt
import networkx as nx


class NetworkSimulator:
    """SIRモデルのシミュレーションを行うクラス"""

    def __init__(self, beta: float, gamma: float):
        """
        初期化
        Args:
            beta (float): 感染率
            gamma (float): 回復率
        """
        self.beta = beta  # 感染率
        self.gamma = gamma  # 回復率

    def run_sir(self, G: nx.Graph, initial_infected: list, num_steps: int) -> dict:
        """
        SIRモデルのシミュレーションを実行
        Args:
            G (nx.Graph): シミュレーション対象のネットワーク
            initial_infected (list): 初期感染ノードのリスト
            num_steps (int): シミュレーションのステップ数
        Returns:
            dict: 各時点でのS,I,Rの数を含む辞書
        """
        # ノードの状態を初期化 (S=0, I=1, R=2)
        states = {node: 0 for node in G.nodes()}
        for node in initial_infected:
            states[node] = 1

        # 結果を記録
        results = {"S": [], "I": [], "R": []}

        # シミュレーション実行
        for step in range(num_steps):
            # 現在の状態を記録
            s = sum(1 for state in states.values() if state == 0)
            i = sum(1 for state in states.values() if state == 1)
            r = sum(1 for state in states.values() if state == 2)
            results["S"].append(s)
            results["I"].append(i)
            results["R"].append(r)

            # 状態更新
            new_states = states.copy()
            for node in G.nodes():
                if states[node] == 0:  # Susceptible
                    # 隣接ノードからの感染をチェック
                    for neighbor in G.neighbors(node):
                        if states[neighbor] == 1 and random.random() < self.beta:
                            new_states[node] = 1
                            break
                elif states[node] == 1:  # Infected
                    # 回復をチェック
                    if random.random() < self.gamma:
                        new_states[node] = 2
            states = new_states

        return results

    def plot_results(self, results: dict, type: str):
        """
        SIRモデルのシミュレーション結果をプロット

        Args:
            results (dict): run_sirメソッドから返された結果辞書
        """
        plt.figure(figsize=(10, 6))
        # 各状態の時系列プロット
        time = range(len(results["S"]))
        plt.plot(time, results["S"], "b-", label="Susceptible")
        plt.plot(time, results["I"], "r-", label="Infected")
        plt.plot(time, results["R"], "g-", label="Recovered")

        # グラフの設定
        plt.xlabel("Time step")
        plt.ylabel("Number of nodes")
        plt.title(f"SIR Model Simulation on {type}")
        plt.grid(True)
        plt.legend()
        plt.show()
