import Base from '../lib/LdrsBaseElement.js';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            'l-ring': {
                size?: number | string;
                color?: number | string;
                speed?: number | string;
                stroke?: number | string;
                'bg-opacity'?: number | string;
            };
        }
    }
}
declare class Ring extends Base {
    _attributes: string[];
    size: string;
    color: string;
    speed: string;
    stroke: string;
    'bg-opacity': string;
    static get observedAttributes(): string[];
    constructor();
    connectedCallback(): void;
    attributeChangedCallback(): void;
}
declare const _default: {
    register: (name?: string) => void;
    element: typeof Ring;
};
export default _default;
//# sourceMappingURL=ring.d.ts.map