# クラスについて

## 今回のクラス設計
1. 単一責任の原則:
- `NetworkGenerator`: ネットワーク生成のみを担当
- `NetworkAnalyzer`: 分析とプロットを担当

2. 疎結合:
- 生成と分析が分離され、独立して変更可能
- 異なる種類のネットワークに対して同じ分析が可能

3. 再利用性:
- 分析機能を他のネットワークタイプにも適用可能
- テストが書きやすい

4. 拡張性:
- 新しい分析手法の追加が容易
- 新しいネットワークタイプの追加が容易

## abstract classのメモ
- `abstractmethod`: Pythonのabc(Abstract Base Class)モジュールで提供されるデコレータ

1. 目的
- 抽象メソッドを定義するために使用
- サブクラスで実装しなければならないメソッドを指定
- サブクラスで実装されていない場合、インスタンス化を防ぐ

2. 使用方法
```python
from abc import ABC, abstractmethod

class NetworkGenerator(ABC):
    @abstractmethod
    def generate(self) -> nx.Graph:
        pass
```

3. 効果
- このデコレータが付いたメソッドを持つクラスは、直接インスタンス化できない
- サブクラスは必ずこのメソッド(今回なら`generate()`)を実装する必要がある
- 実装忘れがある場合、インスタンス化時に TypeError が発生
- これにより、ネットワーク生成の基本インターフェースを強制し、一貫性のある設計を実現

4. 具体例
```python
# ✅ 正しい実装
class SmallWorldNetwork(NetworkGenerator):
    def generate(self) -> nx.Graph:  # abstractmethodを実装
        # 実装内容
        return graph

# ❌ エラーになる実装
class BadNetwork(NetworkGenerator):
    pass  # generateメソッドを実装していないのでエラー
```

# ソースコード部分について

## クラスで実装した抽象メソッドを呼び出す流れ
1. クラス階層の階層
- `NetworkGenerator`: 抽象基底クラス（インターフェース）
- `SmallWorldNetwork`: 具体的な実装を持つ子クラス

2. `abstractmethod`と使用例の関係
- NetworkGeneratorは抽象クラスなので直接インスタンス化できない
- `@abstractmethod`が付いたメソッドは実装を持たない
- 実際の使用時は必ず具体的な実装を持つ子クラス（この場合`SmallWorldNetwork`）を使用する

e.g.
```python
# ❌ これはエラーになる
generator = NetworkGenerator()  # 抽象クラスはインスタンス化できない

# ✅ これが正しい使用方法
generator = SmallWorldNetwork(n_nodes=100, k_neighbors=4)  # 具体的な実装を持つ子クラスを使用
```

>[!NOTE]
> オブジェクト指向設計の基本原則の一つで、具体的な実装は子クラスで行い、親クラスはインターフェースの定義のみを行うという考え方に基づいている!!