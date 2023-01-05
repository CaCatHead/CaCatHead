export function indexToOffset(pid: string) {
  if (/^[A-Z]$/.test(pid)) {
    return pid.charCodeAt(0) - 65;
  } else if (/^[a-z]$/.test(pid)) {
    return pid.charCodeAt(0) - 97;
  } else {
    return undefined;
  }
}

const OFFSET = 1000;

export function displyaIdToIndex(display_id: number) {
  return String.fromCharCode(65 + (display_id - OFFSET));
}
