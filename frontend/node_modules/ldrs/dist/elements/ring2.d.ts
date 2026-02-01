import Base from '../lib/LdrsBaseElement.js';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            'l-ring-2': {
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
declare class Ring2 extends Base {
    _attributes: string[];
    size: string;
    color: string;
    speed: string;
    stroke: string;
    'stroke-length': string;
    'bg-opacity': string;
    static get observedAttributes(): string[];
    constructor();
    connectedCallback(): void;
    attributeChangedCallback(): void;
}
declare const _default: {
    register: (name?: string) => void;
    element: typeof Ring2;
};
export default _default;
//# sourceMappingURL=ring2.d.ts.map