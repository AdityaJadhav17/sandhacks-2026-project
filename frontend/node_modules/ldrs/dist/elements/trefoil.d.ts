import Base from '../lib/LdrsBaseElement.js';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            'l-trefoil': {
                size?: number | string;
                color?: number | string;
                speed?: number | string;
                stroke?: number | string;
                'stroke-length'?: number | string;
                'bg-opacity'?: number | string;
            };
        }
    }
}
declare class Trefoil extends Base {
    _attributes: string[];
    size: string;
    color: string;
    speed: string;
    stroke: string;
    'stroke-length': string;
    'bg-opacity': string;
    d: string;
    static get observedAttributes(): string[];
    constructor();
    connectedCallback(): void;
    attributeChangedCallback(): void;
}
declare const _default: {
    register: (name?: string) => void;
    element: typeof Trefoil;
};
export default _default;
//# sourceMappingURL=trefoil.d.ts.map