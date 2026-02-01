import Base from '../lib/LdrsBaseElement.js';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            'l-treadmill': {
                size?: number | string;
                color?: number | string;
                speed?: number | string;
            };
        }
    }
}
declare class Treadmill extends Base {
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
    element: typeof Treadmill;
};
export default _default;
//# sourceMappingURL=treadmill.d.ts.map