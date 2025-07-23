import { useEffect, useState } from "react";
import "./App.css";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "./components/ui/table";

interface User {
  id: string;  // DynamoDBに合わせて文字列型に変更
  name: string;
  email: string;
}

function App() {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    fetchUsers();
  }, []); // 空の依存配列を渡すことで、コンポーネントのマウント時に一度だけ実行される

  // 2. ユーザー一覧を取得
  const fetchUsers = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL
      const response = await fetch(`${apiUrl}/api/users`);
      const result = await response.json();
      const data: User[] = result.users; // APIレスポンスの構造に合わせて修正
      console.log(data);
      setUsers(data);
      return data;
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  return (
    <div className="flex min-h-svh flex-col items-center justify-center">
      <Table>
        <TableCaption>A list of users.</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="text-center">ID</TableHead>
            <TableHead className="text-center">Name</TableHead>
            <TableHead className="text-center">Email</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {users.map((user) => (
            <TableRow key={user.id}>
              <TableCell className="font-medium text-center">{user.id}</TableCell>
              <TableCell className="text-center">{user.name}</TableCell>
              <TableCell className="text-center">{user.email}</TableCell>
            </TableRow>
          ))}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell colSpan={2} className="text-center">Total Users</TableCell>
            <TableCell className="text-center">{users.length}</TableCell>
          </TableRow>
        </TableFooter>
      </Table>
    </div>
  );
}

export default App;
