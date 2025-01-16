import { ObjectId } from "mongodb"

interface Base {
    _id?: ObjectId
    createdAt: Date
    updatedAt: Date
    deletedAt?: Date | null

}

interface Settings {
    deviceToken: string
    notifications?: boolean | null
    notifyByEmail?: boolean | null
}

export interface User extends Base {
    username?: string | null
    email: string
    settings: Settings
}

export interface Weather extends Base {
    temperature?: number | null
    humidity?: number | null
    pressure?: number | null
    altitude?: number | null

    reader: string
}

export interface Tokens {
    access: string,
    refresh: string,
    user: User,
}