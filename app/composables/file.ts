export const readFileContent = (file: File): Promise<string> => {
  return new Promise(res => {
    const reader = new FileReader();
    reader.addEventListener('loadend', ev => {
      res((ev.target?.result as string) ?? '');
    });
    reader.readAsText(file);
  });
};

export const readFileToU8 = (file: File): Promise<Uint8Array> => {
  return new Promise(res => {
    const reader = new FileReader();
    reader.addEventListener('loadend', ev => {
      const buffer: ArrayBuffer = ev.target?.result! as ArrayBuffer;
      res(new Uint8Array(buffer));
    });
    reader.readAsArrayBuffer(file);
  });
};
