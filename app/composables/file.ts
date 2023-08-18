export const readFileContent = (file: File): Promise<string> => {
  return new Promise(res => {
    const reader = new FileReader();
    reader.addEventListener('loadend', ev => {
      res((ev.target?.result as string) ?? '');
    });
    reader.readAsText(file);
  });
};

export const readFileToU8 = (
  file: File
): Promise<{ data: Uint8Array; length: number }> => {
  return new Promise(res => {
    const reader = new FileReader();
    reader.addEventListener('loadend', ev => {
      const buffer: ArrayBuffer = ev.target?.result! as ArrayBuffer;
      res({ data: new Uint8Array(buffer), length: buffer.byteLength });
    });
    reader.readAsArrayBuffer(file);
  });
};

export const validateFileEncodeing = (data: {
  data: Uint8Array;
  length: number;
}) => {
  const { data: fileBuffer, length: bytesRead } = data;

  // empty file. no clue what it is.
  if (bytesRead === 0) return '';

  // eslint-disable-next-line functional/no-let
  let suspiciousBytes = 0;
  const MAX_BYTES = 512;
  const totalBytes = Math.min(bytesRead, MAX_BYTES);

  // UTF-8 BOM
  if (
    bytesRead >= 3 &&
    fileBuffer[0] === 0xef &&
    fileBuffer[1] === 0xbb &&
    fileBuffer[2] === 0xbf
  )
    return 'UTF-8 BOM';

  // UTF-32 BOM
  if (
    bytesRead >= 4 &&
    fileBuffer[0] === 0x00 &&
    fileBuffer[1] === 0x00 &&
    fileBuffer[2] === 0xfe &&
    fileBuffer[3] === 0xff
  )
    return 'UTF-32 BOM';

  // UTF-32 LE BOM
  if (
    bytesRead >= 4 &&
    fileBuffer[0] === 0xff &&
    fileBuffer[1] === 0xfe &&
    fileBuffer[2] === 0x00 &&
    fileBuffer[3] === 0x00
  )
    return 'UTF-32 LE BOM';

  // GB BOM
  if (
    bytesRead >= 4 &&
    fileBuffer[0] === 0x84 &&
    fileBuffer[1] === 0x31 &&
    fileBuffer[2] === 0x95 &&
    fileBuffer[3] === 0x33
  )
    return 'GB BOM';

  if (totalBytes >= 5 && fileBuffer.slice(0, 5).toString() === '%PDF-') {
    /* PDF. This is binary. */
    return 'PDF';
  }

  // UTF-16 BE BOM
  if (bytesRead >= 2 && fileBuffer[0] === 0xfe && fileBuffer[1] === 0xff)
    return 'UTF-16 BE BOM';

  // UTF-16 LE BOM
  if (bytesRead >= 2 && fileBuffer[0] === 0xff && fileBuffer[1] === 0xfe)
    return 'UTF-16 LE BOM';

  for (let i = 0; i < totalBytes; i++) {
    if (fileBuffer[i] === 0) {
      // NULL byte--it's binary!
      return true;
    } else if (
      (fileBuffer[i] < 7 || fileBuffer[i] > 14) &&
      (fileBuffer[i] < 32 || fileBuffer[i] > 127)
    ) {
      // UTF-8 detection
      if (fileBuffer[i] > 193 && fileBuffer[i] < 224 && i + 1 < totalBytes) {
        i++;
        if (fileBuffer[i] > 127 && fileBuffer[i] < 192) continue;
      } else if (
        fileBuffer[i] > 223 &&
        fileBuffer[i] < 240 &&
        i + 2 < totalBytes
      ) {
        i++;
        if (
          fileBuffer[i] > 127 &&
          fileBuffer[i] < 192 &&
          fileBuffer[i + 1] > 127 &&
          fileBuffer[i + 1] < 192
        ) {
          i++;
          continue;
        }
      }

      suspiciousBytes++;
      // Read at least 32 fileBuffer before making a decision
      if (i >= 32 && (suspiciousBytes * 100) / totalBytes > 10) return true;
    }
  }

  if ((suspiciousBytes * 100) / totalBytes > 10) return 'Binary';

  return 'UTF-8';
};
