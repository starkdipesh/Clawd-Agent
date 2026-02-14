#!/usr/bin/env python3
"""
Phase 2 Messaging Integration Tests
Comprehensive test suite for messaging platform integrations
"""
import requests
import json
import sys
from datetime import datetime

class MessagingIntegrationTester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.user_id = None
        self.bot_ids = {}
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:300]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test API health check"""
        return self.run_test("Health Check", "GET", "api/health", 200)

    def test_create_user(self):
        """Create a test user for messaging tests"""
        user_data = {
            "name": f"Messaging Test User {datetime.now().strftime('%H%M%S')}",
            "email": f"messaging_test_{datetime.now().strftime('%H%M%S')}@example.com"
        }
        success, response = self.run_test("Create User", "POST", "api/users/create", 200, user_data)
        if success and 'user_id' in response:
            self.user_id = response['user_id']
            print(f"   Created user ID: {self.user_id}")
        return success

    # Telegram Bot Tests
    def test_create_telegram_bot(self):
        """Test creating a Telegram bot configuration"""
        if not self.user_id:
            print("❌ No user ID available")
            return False
        
        bot_config = {
            "user_id": self.user_id,
            "platform": "telegram",
            "bot_name": "Test Telegram Bot",
            "bot_token": "MOCK_TOKEN",
            "settings": {"ai_enabled": True}
        }
        success, response = self.run_test(
            "Create Telegram Bot", "POST", "api/messaging/config/create", 200, bot_config
        )
        if success and 'bot_id' in response:
            self.bot_ids['telegram'] = response['bot_id']
        return success

    def test_create_discord_bot(self):
        """Test creating a Discord bot configuration"""
        if not self.user_id:
            print("❌ No user ID available")
            return False
        
        bot_config = {
            "user_id": self.user_id,
            "platform": "discord",
            "bot_name": "Test Discord Bot",
            "bot_token": "MOCK_TOKEN",
            "settings": {"ai_enabled": True}
        }
        success, response = self.run_test(
            "Create Discord Bot", "POST", "api/messaging/config/create", 200, bot_config
        )
        if success and 'bot_id' in response:
            self.bot_ids['discord'] = response['bot_id']
        return success

    def test_create_whatsapp_bot(self):
        """Test creating a WhatsApp bot configuration"""
        if not self.user_id:
            print("❌ No user ID available")
            return False
        
        bot_config = {
            "user_id": self.user_id,
            "platform": "whatsapp",
            "bot_name": "Test WhatsApp Bot",
            "bot_token": "MOCK_TOKEN",
            "settings": {
                "account_sid": "MOCK_SID",
                "auth_token": "MOCK_AUTH",
                "whatsapp_number": "whatsapp:+14155238886"
            }
        }
        success, response = self.run_test(
            "Create WhatsApp Bot", "POST", "api/messaging/config/create", 200, bot_config
        )
        if success and 'bot_id' in response:
            self.bot_ids['whatsapp'] = response['bot_id']
        return success

    def test_create_slack_bot(self):
        """Test creating a Slack bot configuration"""
        if not self.user_id:
            print("❌ No user ID available")
            return False
        
        bot_config = {
            "user_id": self.user_id,
            "platform": "slack",
            "bot_name": "Test Slack Bot",
            "bot_token": "MOCK_TOKEN",
            "settings": {"ai_enabled": True}
        }
        success, response = self.run_test(
            "Create Slack Bot", "POST", "api/messaging/config/create", 200, bot_config
        )
        if success and 'bot_id' in response:
            self.bot_ids['slack'] = response['bot_id']
        return success

    def test_get_user_bots(self):
        """Test retrieving all bots for a user"""
        if not self.user_id:
            print("❌ No user ID available")
            return False
        
        return self.run_test(
            "Get User Bots", "GET", f"api/messaging/config/list/{self.user_id}", 200
        )[0]

    def test_get_specific_bot(self):
        """Test retrieving a specific bot configuration"""
        if not self.bot_ids.get('telegram'):
            print("❌ No Telegram bot ID available")
            return False
        
        bot_id = self.bot_ids['telegram']
        return self.run_test(
            "Get Specific Bot", "GET", f"api/messaging/config/get/{bot_id}", 200
        )[0]

    def test_update_bot_config(self):
        """Test updating bot configuration"""
        if not self.bot_ids.get('telegram'):
            print("❌ No Telegram bot ID available")
            return False
        
        bot_id = self.bot_ids['telegram']
        updates = {
            "bot_name": "Updated Telegram Bot",
            "settings": {"ai_enabled": False, "custom_field": "test"}
        }
        return self.run_test(
            "Update Bot Config", "PUT", f"api/messaging/config/update/{bot_id}", 200, updates
        )[0]

    def test_toggle_bot_disable(self):
        """Test disabling a bot"""
        if not self.bot_ids.get('telegram'):
            print("❌ No Telegram bot ID available")
            return False
        
        bot_id = self.bot_ids['telegram']
        return self.run_test(
            "Disable Bot", "PUT", f"api/messaging/config/toggle/{bot_id}", 200, {"enabled": False}
        )[0]

    def test_toggle_bot_enable(self):
        """Test re-enabling a bot"""
        if not self.bot_ids.get('telegram'):
            print("❌ No Telegram bot ID available")
            return False
        
        bot_id = self.bot_ids['telegram']
        return self.run_test(
            "Enable Bot", "PUT", f"api/messaging/config/toggle/{bot_id}", 200, {"enabled": True}
        )[0]

    def test_send_message_telegram(self):
        """Test sending a message through Telegram bot"""
        if not self.bot_ids.get('telegram'):
            print("❌ No Telegram bot ID available")
            return False
        
        bot_id = self.bot_ids['telegram']
        message_data = {
            "recipient": "123456789",
            "message": "Hello from Moltbot test suite!",
            "metadata": {"test": True}
        }
        return self.run_test(
            "Send Telegram Message", "POST", f"api/messaging/send/{bot_id}", 200, message_data
        )[0]

    def test_send_message_discord(self):
        """Test sending a message through Discord bot"""
        if not self.bot_ids.get('discord'):
            print("❌ No Discord bot ID available")
            return False
        
        bot_id = self.bot_ids['discord']
        message_data = {
            "recipient": "987654321",
            "message": "Hello Discord from Moltbot!",
            "metadata": {}
        }
        return self.run_test(
            "Send Discord Message", "POST", f"api/messaging/send/{bot_id}", 200, message_data
        )[0]

    def test_send_message_whatsapp(self):
        """Test sending a message through WhatsApp bot"""
        if not self.bot_ids.get('whatsapp'):
            print("❌ No WhatsApp bot ID available")
            return False
        
        bot_id = self.bot_ids['whatsapp']
        message_data = {
            "recipient": "whatsapp:+1234567890",
            "message": "Hello WhatsApp from Moltbot!",
            "metadata": {}
        }
        return self.run_test(
            "Send WhatsApp Message", "POST", f"api/messaging/send/{bot_id}", 200, message_data
        )[0]

    def test_send_message_slack(self):
        """Test sending a message through Slack bot"""
        if not self.bot_ids.get('slack'):
            print("❌ No Slack bot ID available")
            return False
        
        bot_id = self.bot_ids['slack']
        message_data = {
            "recipient": "C1234567890",
            "message": "Hello Slack from Moltbot!",
            "metadata": {}
        }
        return self.run_test(
            "Send Slack Message", "POST", f"api/messaging/send/{bot_id}", 200, message_data
        )[0]

    def test_get_message_history(self):
        """Test retrieving message history"""
        if not self.bot_ids.get('telegram'):
            print("❌ No Telegram bot ID available")
            return False
        
        bot_id = self.bot_ids['telegram']
        return self.run_test(
            "Get Message History", "GET", f"api/messaging/messages/{bot_id}?limit=10", 200
        )[0]

    def test_duplicate_bot_prevention(self):
        """Test that duplicate bots for same platform are prevented"""
        if not self.user_id:
            print("❌ No user ID available")
            return False
        
        bot_config = {
            "user_id": self.user_id,
            "platform": "telegram",
            "bot_name": "Duplicate Bot",
            "bot_token": "MOCK_TOKEN_2",
            "settings": {}
        }
        success, _ = self.run_test(
            "Duplicate Bot Prevention", "POST", "api/messaging/config/create", 400, bot_config
        )
        # For this test, we expect it to fail (400), so invert success
        return not success

    def test_delete_bot(self):
        """Test deleting a bot configuration"""
        if not self.bot_ids.get('slack'):
            print("❌ No Slack bot ID available")
            return False
        
        bot_id = self.bot_ids['slack']
        return self.run_test(
            "Delete Bot", "DELETE", f"api/messaging/config/delete/{bot_id}", 200
        )[0]

    def test_webhook_endpoints_exist(self):
        """Test that webhook endpoints are accessible"""
        print("\n🔍 Testing Webhook Endpoints Accessibility...")
        
        # These will return errors without proper data, but should not be 404
        endpoints_ok = True
        
        # Telegram webhook (should exist)
        try:
            response = requests.post(f"{self.base_url}/api/messaging/webhook/telegram/test-bot-id")
            if response.status_code != 404:
                print("   ✅ Telegram webhook endpoint exists")
            else:
                print("   ❌ Telegram webhook endpoint not found")
                endpoints_ok = False
        except:
            endpoints_ok = False
        
        # Discord webhook
        try:
            response = requests.post(f"{self.base_url}/api/messaging/webhook/discord/test-bot-id")
            if response.status_code != 404:
                print("   ✅ Discord webhook endpoint exists")
            else:
                print("   ❌ Discord webhook endpoint not found")
                endpoints_ok = False
        except:
            endpoints_ok = False
        
        return endpoints_ok


def main():
    print("🚀 Starting Phase 2 - Messaging Integration Tests...")
    print("=" * 60)
    tester = MessagingIntegrationTester()

    # Test sequence
    tests = [
        ("Health Check", tester.test_health_check),
        ("Create User", tester.test_create_user),
        ("Create Telegram Bot", tester.test_create_telegram_bot),
        ("Create Discord Bot", tester.test_create_discord_bot),
        ("Create WhatsApp Bot", tester.test_create_whatsapp_bot),
        ("Create Slack Bot", tester.test_create_slack_bot),
        ("Get User Bots", tester.test_get_user_bots),
        ("Get Specific Bot", tester.test_get_specific_bot),
        ("Update Bot Config", tester.test_update_bot_config),
        ("Disable Bot", tester.test_toggle_bot_disable),
        ("Enable Bot", tester.test_toggle_bot_enable),
        ("Send Telegram Message", tester.test_send_message_telegram),
        ("Send Discord Message", tester.test_send_message_discord),
        ("Send WhatsApp Message", tester.test_send_message_whatsapp),
        ("Send Slack Message", tester.test_send_message_slack),
        ("Get Message History", tester.test_get_message_history),
        ("Duplicate Bot Prevention", tester.test_duplicate_bot_prevention),
        ("Delete Bot", tester.test_delete_bot),
        ("Webhook Endpoints", tester.test_webhook_endpoints_exist),
    ]

    # Run all tests
    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")

    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Final Results:")
    print(f"   Tests Run: {tester.tests_run}")
    print(f"   Tests Passed: {tester.tests_passed}")
    print(f"   Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"   Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    print("=" * 60)
    
    if tester.user_id:
        print(f"\n👤 Test User Created: {tester.user_id}")
    
    if tester.bot_ids:
        print(f"🤖 Bots Created: {len(tester.bot_ids)}")
        for platform, bot_id in tester.bot_ids.items():
            print(f"   - {platform}: {bot_id}")
    
    print("\n✅ Phase 2 Testing Complete!")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
