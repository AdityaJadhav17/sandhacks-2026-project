import Base from '../lib/LdrsBaseElement.js';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            'l-hatch': {
                size?: number | string;
                color?: number | string;
                speed?: number | string;
                stroke?: number | string;
            };
        }
    }
}
declare class Hatch extends Base {
    _attributes: string[];
    size: string;
    color: string;
    speed: string;
    stroke: string;
    static get observedAttributes(): string[];
    constructor();
    connectedCallback(): void;
    attributeChangedCallback(): void;
}
declare const _default: {
    register: (name?: string) => void;
    element: typeof Hatch;
};
export default _default;
//# sourceMappingURL=hatch.d.ts.map