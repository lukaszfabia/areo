import { ObjectId } from "mongodb"

interface Base {
    _id?: ObjectId | string
    created_at: Date | string
    updated_at: Date | string
    deleted_at?: Date | null | string
}

interface Settings {
    device_token: string
    notifications?: boolean | null
    notify_by_email?: boolean | null
}

export interface User extends Base {
    username?: string | null
    email: string
    password: string
    settings?: Settings | null
}

export interface Weather extends Base {
    temperature?: number | null
    humidity?: number | null
    pressure?: number | null
    altitude?: number | null

    reader: string
}

export interface Tokens {
    user: User,
    access_token: string,
    refresh_token: string,
}