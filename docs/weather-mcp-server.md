weather-mcp-server
TypeScript icon, indicating that this package has built-in type declarations
2.4.0 • Public • Published 22 days ago
Weather MCP Server
MCP (Model Context Protocol) サーバーでAIアシスタント（Claude、Clineなど）に天気情報を提供するパッケージです。

🌟 特徴
リアルタイム天気情報: 指定した場所の現在の天気を取得
MCPプロトコル準拠: Claude、ClineなどのAIアシスタントとシームレスに連携
TypeScript実装: 型安全で信頼性の高いコードベース
柔軟な設定: ダミーデータまたは実際の天気APIとの統合が可能
軽量高速: 最小限の依存関係で高速なレスポンス
🚀 クイックスタート
インストール
npm install @duwenji/weather-mcp-server
Clineでの使用方法
Clineの設定ファイルに追加:
{
  "weather-server": {
    "autoApprove": [],
    "disabled": false,
    "timeout": 60,
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "@duwenji/weather-mcp-server"
    ],
    "env": {
      "OPENWEATHER_API_KEY": "your_api_key_here"
    }
  }
}
Clineを再起動

天気情報を取得:

@weather-server get_weather location="東京"
または自然言語で:

東京の天気を教えてください
📋 提供されるツール
get_weather
指定した場所の現在の天気情報を取得します。

パラメータ:

location (必須): 都市名または場所（例: "Tokyo", "大阪", "New York"）
使用例:

{
  "location": "Tokyo"
}
レスポンス例:

{
  "content": [
    {
      "type": "text",
      "text": "Weather in Tokyo: 25°C, 晴れ, 湿度: 65%, 風速: 5km/h"
    }
  ]
}
🛠️ 開発者向け
サーバー実行方法
# MCPサーバーとして実行
npx weather-mcp-server

# 開発モード（TypeScript直接実行）
npm run dev

# ビルド
npm run build

# 実行（ビルド後）
npm start

# クリーン（distディレクトリ削除）
npm run clean
依存関係のインストール
npm install
🔧 設定
環境変数を使用して設定をカスタマイズできます:

# 実際の天気APIを使用する場合
export OPENWEATHER_API_KEY=your_api_key
📊 使用例
Clineとの連携例
ユーザー: 東京の天気は？
Cline: @weather-server get_weather location="東京"
天気サーバー: Weather in Tokyo: 22°C, 曇り, 降水確率: 30%
Cline: 東京の天気は22度で曇り、降水確率は30%です。
複数都市の天気比較
ユーザー: 東京と大阪の天気を比較して
Cline: @weather-server get_weather location="東京"
天気サーバー: Weather in Tokyo: 25°C, 晴れ
Cline: @weather-server get_weather location="大阪"  
天気サーバー: Weather in Osaka: 26°C, 曇り
Cline: 東京は25度で晴れ、大阪は26度で曇りです。気温はほぼ同じですが、大阪は曇り空です。
🤝 貢献
バグレポート、機能リクエスト、プルリクエストは歓迎します！

リポジトリをフォーク
機能ブランチを作成 (git checkout -b feature/amazing-feature)
変更をコミット (git commit -m 'Add amazing feature')
ブランチにプッシュ (git push origin feature/amazing-feature)
プルリクエストを作成
📄 ライセンス
このプロジェクトはMITライセンスの下で公開されています - 詳細はLICENSEファイルを参照してください。

🔗 関連リンク
Model Context Protocol 公式サイト
npm パッケージページ
GitHub リポジトリ
Readme
Keywords
mcp-serverweather-mcpmodel-context-protocolweather-apiclaude-weatherai-weathermcp-weather-serverweather-informationai-assistantcline-tools
Package Sidebar
Install
npm i @duwenji/weather-mcp-server


Repository
github.com/duwenji/weather-server

Homepage
github.com/duwenji/weather-server#readme