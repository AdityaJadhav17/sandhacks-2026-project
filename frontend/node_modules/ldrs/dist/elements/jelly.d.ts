import Base from '../lib/LdrsBaseElement.js';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            'l-jelly': {
                size?: number | string;
                color?: number | string;
                speed?: number | string;
            };
        }
    }
}
declare class Jelly extends Base {
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
    element: typeof Jelly;
};
export default _default;
//# sourceMappingURL=jelly.d.ts.map