# クラス設計のルール
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