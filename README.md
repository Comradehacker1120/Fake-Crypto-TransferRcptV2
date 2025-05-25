# Fake-Crypto-TransferRcptV2

# Fake Crypto Transfer Pro (Telegram Bot)

A sophisticated Python script that generates highly realistic fake cryptocurrency transaction receipts with QR codes, blockchain explorer links, and comprehensive transaction details. Designed to work as an interactive Telegram bot.

## 🌟 Features

- **Multi-Currency Support**:
  - Bitcoin (BTC)
  - Ethereum (ETH)
  - Tether (USDT-ERC20)
  - Dogecoin (DOGE)
  - Monero (XMR)

- **Professional Receipts**:
  - Realistic transaction IDs
  - QR codes for wallet addresses
  - Blockchain explorer links
  - Fiat value estimates
  - Network confirmation status
  - Detailed transaction metadata
  - Memo/note support

- **Enhanced Realism**:
  - Cryptocurrency-specific address generation
  - Dynamic exchange rates
  - Network-specific fees
  - Transaction size and block height
  - Timestamp with relative time
  - Progress indicators

- **User-Friendly Interface**:
  - Interactive Telegram bot
  - Inline keyboard for crypto selection
  - Input validation
  - Error handling
  - Markdown formatting

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- Telegram account
- Basic terminal knowledge

### Installation

1. Clone the repository or download the script:
   ```bash
   git clone https://github.com/Comradehacker1120/Fake-Crypto-TransferRcptV2
   cd Fake-Crypto-TransferRcptV2 
   ```

2. Install required dependencies:
   ```bash
   pip3 install python-telegram-bot faker qrcode[pil]
   ```

3. Run the script:
   ```bash
   python fakecryptotransferV2.py
   ```

### Bot Configuration

1. **Create a Telegram Bot**:
   - Start a chat with [@BotFather](https://t.me/BotFather) on Telegram
   - Use `/newbot` command to create a new bot
   - Copy the API token provided

2. **Get Your Chat ID**:
   - Start a chat with [@userinfobot](https://t.me/userinfobot) on Telegram
   - It will reply with your chat ID

3. **First Run Setup**:
   - When you first run the script, it will prompt you for:
     - Your bot token (from @BotFather)
     - Your chat ID (from @userinfobot)
   - This information will be saved in `crypto_prank_pro_config.json`

## 🤖 Usage Guide

### Telegram Commands

- `/start` - Show welcome message
- `/generate` - Start creating a fake transaction
- `/settings` - View current bot configuration
- `/help` - Show help information

### Transaction Generation Flow

1. Send `/generate` to start
2. Select cryptocurrency using inline buttons
3. Enter recipient address (or use `/random` for auto-generation)
4. Enter amount to send (with validation)
5. (Optional) Add transaction memo or `/skip`
6. Receive generated transaction receipt as HTML file

### Example Transaction

```plaintext
✅ Fake Bitcoin Transaction Generated!

▪️ Amount: 0.042 BTC
▪️ To: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
▪️ Fee: 0.0005 BTC
▪️ Ref ID: TRX100123
▪️ Memo: Payment for services

📁 Receipt saved as: prank_receipts/btc_tx_TRX100123_1623456789.html
```

## ⚙️ Customization Options

You can modify:

1. **Exchange Rates**:
   - Edit `exchange_rates` in `crypto_prank_pro_config.json`

2. **Network Fees**:
   - Adjust `network_fees` in the config file

3. **Receipt Appearance**:
   - Modify the `HTML_TEMPLATE` in the script
   - Change colors, layout, or information displayed

4. **Supported Cryptocurrencies**:
   - Add/remove coins from `CRYPTO_DATA` dictionary
   - Ensure to include all required fields

## 📸 Sample Output

![Sample Receipt](sample_receipt.png) *(Example transaction receipt)*

## ⚠️ Important Disclaimer

- This tool is for **educational and demonstration purposes only**
- Do **not** use to deceive or scam anyone
- Generated transactions are completely fake and not connected to any real blockchain
- The author is **not responsible** for any misuse of this tool
- Use responsibly and ethically

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Support

For issues or feature requests, please [open an issue] or contact the developer.

---

🚀 Enjoy generating ultra-realistic fake crypto transactions! Remember to use responsibly.
