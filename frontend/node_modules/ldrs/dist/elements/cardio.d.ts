import Base from '../lib/LdrsBaseElement.js';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            'l-cardio': {
                size?: number | string;
                color?: number | string;
                speed?: number | string;
                stroke?: number | string;
                'bg-opacity'?: number | string;
            };
        }
    }
}
declare class Cardio extends Base {
    _attributes: string[];
    size: string;
    color: string;
    speed: string;
    stroke: string;
    'bg-opacity': string;
    d: string;
    static get observedAttributes(): string[];
    constructor();
    connectedCallback(): void;
    attributeChangedCallback(): void;
}
declare const _default: {
    register: (name?: string) => void;
    element: typeof Cardio;
};
export default _default;
//# sourceMappingURL=cardio.d.ts.map