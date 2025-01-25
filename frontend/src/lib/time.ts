import { Time } from "@internationalized/date";
import { formatDistanceToNow } from "date-fns";

export function transformTime(time: Date): string {
    return `${formatDistanceToNow(time)} ago`;
}

export function toTime(obj: Record<string, number>): Time {
    const t = {
        hour: obj.hour,
        minute: obj.minute,
        second: obj.second,
        millisecond: obj.millisecond,
    } as Time

    return t
}