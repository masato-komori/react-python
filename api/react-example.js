// React側でFastAPIと通信するサンプルコード

// 1. GETリクエストの例
const fetchMessage = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/message');
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error('Error fetching message:', error);
  }
};

// 2. ユーザー一覧を取得
const fetchUsers = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/users');
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

// 3. POSTリクエストでユーザーを作成
const createUser = async (userData) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData)
    });
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error('Error creating user:', error);
  }
};

// 使用例
// fetchMessage();
// fetchUsers();
// createUser({ name: "テストユーザー", email: "test@example.com", age: 25 });

// React Componentの例
/*
import React, { useState, useEffect } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({ name: '', email: '', age: '' });

  useEffect(() => {
    // コンポーネントマウント時にデータを取得
    fetchMessage().then(data => setMessage(data.message));
    fetchUsers().then(data => setUsers(data.users));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userData = {
      name: newUser.name,
      email: newUser.email,
      age: newUser.age ? parseInt(newUser.age) : null
    };
    
    const createdUser = await createUser(userData);
    if (createdUser) {
      alert('ユーザーが作成されました！');
      setNewUser({ name: '', email: '', age: '' });
    }
  };

  return (
    <div className="App">
      <h1>FastAPI + React 通信テスト</h1>
      
      <div>
        <h2>APIからのメッセージ:</h2>
        <p>{message}</p>
      </div>

      <div>
        <h2>ユーザー一覧:</h2>
        <ul>
          {users.map(user => (
            <li key={user.id}>
              {user.name} ({user.email})
            </li>
          ))}
        </ul>
      </div>

      <div>
        <h2>新しいユーザーを作成:</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="名前"
            value={newUser.name}
            onChange={(e) => setNewUser({...newUser, name: e.target.value})}
            required
          />
          <input
            type="email"
            placeholder="メールアドレス"
            value={newUser.email}
            onChange={(e) => setNewUser({...newUser, email: e.target.value})}
            required
          />
          <input
            type="number"
            placeholder="年齢"
            value={newUser.age}
            onChange={(e) => setNewUser({...newUser, age: e.target.value})}
          />
          <button type="submit">作成</button>
        </form>
      </div>
    </div>
  );
}

export default App;
*/
