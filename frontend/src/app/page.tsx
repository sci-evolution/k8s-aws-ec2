import TaskList from "../../components/TaskList";

const mockTasks = [
  { id: 1, title: "Set up project structure" },
  { id: 2, title: "Implement backend API" },
  { id: 3, title: "Build frontend UI" },
];

export default function Home() {
  return <TaskList tasks={mockTasks} />;
}
