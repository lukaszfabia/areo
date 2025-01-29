"use client";
import { useAuth } from "@/providers/Auth";
import { faIdCard } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button } from "@heroui/react";
import { Link } from "@heroui/react"
import { redirect } from "next/navigation";

export default function RfidAuth() {
    const { user, rfidAuth, isLoading, error } = useAuth();

    if (user) {
        redirect("/profile")
    }

    return (
        <div className="space-y-4">
            <h1 className="font-extrabold text-3xl">
                Login via RFID card
            </h1>

            <div className="flex items-center justify-center">
                <Button color="secondary" variant="solid" isLoading={isLoading} onPress={rfidAuth}>
                    Use RFID auth
                    <FontAwesomeIcon icon={faIdCard} />
                </Button>
            </div>
            <p className="text-gray-400 text-center">Click the button and then bring the card close to the device.</p>

            {error && (
                <div className="text-center space-y-5">
                    <p className="text-red-600 animate-pulse">{error}</p>
                    <p>Just <Link href="/login">login</Link> with e-mail</p>
                </div>
            )}
        </div>
    )
}