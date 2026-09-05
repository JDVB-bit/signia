import { useState } from 'react'

function Sidebar() {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
    };
}
