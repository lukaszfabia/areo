"use client";

import { api } from "@/lib/api";
import { Tokens, User } from "@/lib/models"
import { clearStorage, saveCredentials } from "@/lib/token";
import { createContext, FC, ReactNode, useCallback, useContext, useEffect, useState } from "react";


interface AuthProps {
    email: string,
    password: string
    rememberMe: boolean

    // is login or sign up form 
    onCreate: boolean
}

type AuthCtxProps = {
    /* Attrs */
    user?: User | null;
    isLoading: boolean;
    error?: string | null,

    /* Methods */
    logout: () => void;
    auth: (data: AuthProps) => void;
    refresh: () => void;
}

const AuthCtx = createContext<AuthCtxProps>({
    user: null,
    isLoading: false,
    error: null,
    logout: () => { },
    auth: async () => { },
    refresh: async () => { },
})


export interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null | undefined>(null);

    useEffect(() => { !user && refresh() }, [])

    // Get or Create user 
    const auth = useCallback(async (data: AuthProps) => {
        setIsLoading(true);

        try {
            const result = await api<Tokens>({
                method: "POST",
                endpoint: "/api/user/",
                body: data,
            })

            if (result.status === "success" && result.data) {
                setUser(result.data.user)
                saveCredentials(data.rememberMe, result.data)
            } else {
                setError(result.error)
            }


        } catch (err) {
            setError("Unknown error")
        } finally {
            setIsLoading(false);
        }
    }, []);


    const logout = useCallback(() => {
        setIsLoading(true);
        clearStorage();
        setUser(null);
        setIsLoading(false);
    }, []);


    // Uses token to identify user on a server 
    const refresh = useCallback(async () => {
        setIsLoading(true);

        try {
            const result = await api<User>({
                endpoint: "/api/user/",
            })

            if (result.status === "success" && result.data) {
                setUser(result.data)
            } else {
                setError(result.error)
            }


        } catch (err) {
            setError("Unknown error")
        } finally {
            setIsLoading(false);
        }
    }, [])


    return (
        <AuthCtx.Provider value={{
            user,
            isLoading,
            error,
            logout,
            auth,
            refresh,
        }}>
            {children}
        </AuthCtx.Provider>
    )

}

export const useAuth = () => {
    const context = useContext(AuthCtx);
    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};
