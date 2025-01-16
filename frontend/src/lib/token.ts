import { Tokens } from "./models"

// Keys to tokens in browser
export const REFRESH: string = "refresh"
export const ACCESS: string = "access"

export const REFRESH_TOKEN: string | null = localStorage.getItem(REFRESH) ?? sessionStorage.getItem(REFRESH) ?? null
export const ACCESS_TOKEN: string | null = localStorage.getItem(ACCESS) ?? sessionStorage.getItem(ACCESS) ?? null


export const saveCredentials = (remember: boolean, tokens: Tokens) => {
    const storage = remember ? localStorage : sessionStorage
    storage.setItem(ACCESS, tokens.access)
    storage.setItem(REFRESH, tokens.refresh)
}

export const clearStorage = () => {
    localStorage.clear()
    sessionStorage.clear()
}
