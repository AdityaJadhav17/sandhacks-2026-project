import Base from '../lib/LdrsBaseElement.js';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            'l-hourglass': {
                size?: number | string;
                color?: number | string;
                speed?: number | string;
                'bg-opacity'?: number | string;
            };
        }
    }
}
declare class Hourglass extends Base {
    _attributes: string[];
    size: string;
    color: string;
    speed: string;
    'bg-opacity': string;
    static get observedAttributes(): string[];
    constructor();
    connectedCallback(): void;
    attributeChangedCallback(): void;
}
declare const _default: {
    register: (name?: string) => void;
    element: typeof Hourglass;
};
export default _default;
//# sourceMappingURL=hourglass.d.ts.map