import requests
import sys
import json
from datetime import datetime
import uuid

class MoltbotAPITester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.conversation_id = None
        self.task_id = None

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
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
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
        """Test health check endpoint"""
        return self.run_test("Health Check", "GET", "api/health", 200)

    def test_root_endpoint(self):
        """Test root endpoint"""
        return self.run_test("Root Endpoint", "GET", "", 200)

    def test_create_user(self):
        """Test user creation"""
        user_data = {
            "name": f"Test User {datetime.now().strftime('%H%M%S')}",
            "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com"
        }
        success, response = self.run_test("Create User", "POST", "api/users/create", 200, user_data)
        if success and 'user_id' in response:
            self.user_id = response['user_id']
            print(f"   Created user ID: {self.user_id}")
        return success

    def test_get_user(self):
        """Test get user by ID"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
        return self.run_test("Get User", "GET", f"api/users/get/{self.user_id}", 200)[0]

    def test_create_task(self):
        """Test task creation"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
        
        task_data = {
            "user_id": self.user_id,
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "medium",
            "due_date": "2024-12-31T23:59:59"
        }
        success, response = self.run_test("Create Task", "POST", "api/tasks/create", 200, task_data)
        if success and 'task_id' in response:
            self.task_id = response['task_id']
        return success

    def test_get_tasks(self):
        """Test get user tasks"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
        return self.run_test("Get Tasks", "GET", f"api/tasks/list/{self.user_id}", 200)[0]

    def test_update_task(self):
        """Test task update"""
        if not self.task_id:
            print("❌ No task ID available for testing")
            return False
        
        return self.run_test("Complete Task", "PUT", f"api/tasks/complete/{self.task_id}", 200)[0]

    def test_get_skills(self):
        """Test get available skills"""
        return self.run_test("Get Skills", "GET", "api/skills/list", 200)[0]

    def test_get_user_skills(self):
        """Test get user skills"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
        return self.run_test("Get User Skills", "GET", f"api/skills/{self.user_id}", 200)[0]

    def test_toggle_skill(self):
        """Test toggle skill for user"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
        
        # First get available skills
        success, skills_response = self.run_test("Get Skills for Toggle", "GET", "api/skills", 200)
        if success and skills_response.get('skills'):
            skill_id = skills_response['skills'][0]['id']
            toggle_data = {"enabled": True}
            return self.run_test("Toggle Skill", "PUT", f"api/skills/{self.user_id}/{skill_id}", 200, toggle_data)[0]
        return False

    def test_chat_message(self):
        """Test sending chat message"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
        
        chat_data = {
            "user_id": self.user_id,
            "message": "Hello, this is a test message"
        }
        success, response = self.run_test("Send Chat Message", "POST", "api/chat/message", 200, chat_data)
        if success and 'conversation_id' in response:
            self.conversation_id = response['conversation_id']
        return success

    def test_get_conversations(self):
        """Test get user conversations"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
        return self.run_test("Get Conversations", "GET", f"api/chat/conversations/{self.user_id}", 200)[0]

    def test_get_conversation_messages(self):
        """Test get conversation messages"""
        if not self.conversation_id:
            print("❌ No conversation ID available for testing")
            return False
        return self.run_test("Get Conversation Messages", "GET", f"api/chat/messages/{self.conversation_id}", 200)[0]

    def test_get_memory(self):
        """Test get user memory"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
        return self.run_test("Get Memory", "GET", f"api/memory/get/{self.user_id}", 200)[0]

    def test_update_memory(self):
        """Test update user memory"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
        
        memory_data = {
            "user_id": self.user_id,
            "key": "test_preference",
            "value": "test_value"
        }
        return self.run_test("Store Memory", "POST", "api/memory/store", 200, memory_data)[0]

    def test_get_notifications(self):
        """Test get user notifications"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
        return self.run_test("Get Notifications", "GET", f"api/notifications/list/{self.user_id}", 200)[0]

def main():
    print("🚀 Starting Moltbot API Tests...")
    tester = MoltbotAPITester()

    # Test sequence
    tests = [
        ("Health Check", tester.test_health_check),
        ("Root Endpoint", tester.test_root_endpoint),
        ("Create User", tester.test_create_user),
        ("Get User", tester.test_get_user),
        ("Create Task", tester.test_create_task),
        ("Get Tasks", tester.test_get_tasks),
        ("Update Task", tester.test_update_task),
        ("Get Skills", tester.test_get_skills),
        ("Get User Skills", tester.test_get_user_skills),
        ("Toggle Skill", tester.test_toggle_skill),
        ("Chat Message", tester.test_chat_message),
        ("Get Conversations", tester.test_get_conversations),
        ("Get Conversation Messages", tester.test_get_conversation_messages),
        ("Get Memory", tester.test_get_memory),
        ("Update Memory", tester.test_update_memory),
        ("Get Notifications", tester.test_get_notifications),
    ]

    # Run all tests
    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")

    # Print final results
    print(f"\n📊 Final Results:")
    print(f"   Tests Run: {tester.tests_run}")
    print(f"   Tests Passed: {tester.tests_passed}")
    print(f"   Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"   Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.user_id:
        print(f"\n👤 Test User Created: {tester.user_id}")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())