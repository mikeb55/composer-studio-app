declare module 'verovio/wasm' {
  const createVerovioModule: () => Promise<unknown>
  export default createVerovioModule
}

declare module 'verovio/esm' {
  export class VerovioToolkit {
    constructor(module: unknown)
    setOptions(options: string): void
    loadData(data: string): boolean
    getPageCount(): number
    getLog(): string
    redoLayout(options: string): void
    renderToSVG(pageNo: number, xmlDeclaration?: number): string
  }
}
