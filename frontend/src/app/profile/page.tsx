"use client";

import Loading from "@/components/ui/Spinner";
import { useAuth } from "@/providers/Auth";
import Login from "../login/page";

export default function Profile() {
    const { user, isLoading } = useAuth();

    if (!user) return <Login />
    if (isLoading) return <Loading />

    return (
        <div>
            Hello {user.email}
        </div>
    )
}