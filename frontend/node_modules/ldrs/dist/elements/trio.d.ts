import Base from '../lib/LdrsBaseElement.js';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            'l-trio': {
                size?: number | string;
                color?: number | string;
                speed?: number | string;
            };
        }
    }
}
declare class Trio extends Base {
    _attributes: string[];
    size: string;
    color: string;
    speed: string;
    static get observedAttributes(): string[];
    constructor();
    connectedCallback(): void;
    attributeChangedCallback(): void;
}
declare const _default: {
    register: (name?: string) => void;
    element: typeof Trio;
};
export default _default;
//# sourceMappingURL=trio.d.ts.map