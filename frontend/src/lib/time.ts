import { formatDistanceToNow } from "date-fns";

export function transformTime(time: Date): string {
    return `${formatDistanceToNow(time)} ago`;
}