import { Time } from "@internationalized/date"
import { ObjectId } from "mongodb"

interface Base {
    _id?: ObjectId | string
    created_at: Date
    updated_at: Date
    deleted_at?: Date | null
}

export interface Settings {
    rfid_uid?: string | null
    device_token: string
    notifications?: boolean | null
    notify_by_email?: boolean | null

    times?: Time[] | null
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
    user: User
    access_token: string
    refresh_token: string
}

export interface WeatherPaginated {
    data: Weather[]
    pagination: PaginationInfo
}

interface PaginationInfo {
    page: number
    limit: number
    total_items: number
    total_pages: number
}
