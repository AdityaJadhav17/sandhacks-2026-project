import Base from '../lib/LdrsBaseElement.js';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            'l-pinwheel': {
                size?: number | string;
                color?: number | string;
                speed?: number | string;
                stroke?: number | string;
            };
        }
    }
}
declare class Pinwheel extends Base {
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
    element: typeof Pinwheel;
};
export default _default;
//# sourceMappingURL=pinwheel.d.ts.map