/*! *****************************************************************************
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0

THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
MERCHANTABLITY OR NON-INFRINGEMENT.

See the Apache Version 2.0 License for specific language governing permissions
and limitations under the License.
***************************************************************************** */
function t(t,e,n,i){var s,o=arguments.length,r=o<3?e:null===i?i=Object.getOwnPropertyDescriptor(e,n):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(t,e,n,i);else for(var a=t.length-1;a>=0;a--)(s=t[a])&&(r=(o<3?s(r):o>3?s(e,n,r):s(e,n))||r);return o>3&&r&&Object.defineProperty(e,n,r),r
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */}const e=new WeakMap,n=t=>"function"==typeof t&&e.has(t),i=void 0!==window.customElements&&void 0!==window.customElements.polyfillWrapFlushCallback,s=(t,e,n=null)=>{for(;e!==n;){const n=e.nextSibling;t.removeChild(e),e=n}},o={},r={},a=`{{lit-${String(Math.random()).slice(2)}}}`,c=`\x3c!--${a}--\x3e`,l=new RegExp(`${a}|${c}`);class d{constructor(t,e){this.parts=[],this.element=e;const n=[],i=[],s=document.createTreeWalker(e.content,133,null,!1);let o=0,r=-1,c=0;const{strings:d,values:{length:h}}=t;for(;c<h;){const t=s.nextNode();if(null!==t){if(r++,1===t.nodeType){if(t.hasAttributes()){const e=t.attributes,{length:n}=e;let i=0;for(let t=0;t<n;t++)u(e[t].name,"$lit$")&&i++;for(;i-- >0;){const e=d[c],n=m.exec(e)[2],i=n.toLowerCase()+"$lit$",s=t.getAttribute(i);t.removeAttribute(i);const o=s.split(l);this.parts.push({type:"attribute",index:r,name:n,strings:o}),c+=o.length-1}}"TEMPLATE"===t.tagName&&(i.push(t),s.currentNode=t.content)}else if(3===t.nodeType){const e=t.data;if(e.indexOf(a)>=0){const i=t.parentNode,s=e.split(l),o=s.length-1;for(let e=0;e<o;e++){let n,o=s[e];if(""===o)n=p();else{const t=m.exec(o);null!==t&&u(t[2],"$lit$")&&(o=o.slice(0,t.index)+t[1]+t[2].slice(0,-"$lit$".length)+t[3]),n=document.createTextNode(o)}i.insertBefore(n,t),this.parts.push({type:"node",index:++r})}""===s[o]?(i.insertBefore(p(),t),n.push(t)):t.data=s[o],c+=o}}else if(8===t.nodeType)if(t.data===a){const e=t.parentNode;null!==t.previousSibling&&r!==o||(r++,e.insertBefore(p(),t)),o=r,this.parts.push({type:"node",index:r}),null===t.nextSibling?t.data="":(n.push(t),r--),c++}else{let e=-1;for(;-1!==(e=t.data.indexOf(a,e+1));)this.parts.push({type:"node",index:-1}),c++}}else s.currentNode=i.pop()}for(const t of n)t.parentNode.removeChild(t)}}const u=(t,e)=>{const n=t.length-e.length;return n>=0&&t.slice(n)===e},h=t=>-1!==t.index,p=()=>document.createComment(""),m=/([ \x09\x0a\x0c\x0d])([^\0-\x1F\x7F-\x9F "'>=/]+)([ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*))$/;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
class f{constructor(t,e,n){this.__parts=[],this.template=t,this.processor=e,this.options=n}update(t){let e=0;for(const n of this.__parts)void 0!==n&&n.setValue(t[e]),e++;for(const t of this.__parts)void 0!==t&&t.commit()}_clone(){const t=i?this.template.element.content.cloneNode(!0):document.importNode(this.template.element.content,!0),e=[],n=this.template.parts,s=document.createTreeWalker(t,133,null,!1);let o,r=0,a=0,c=s.nextNode();for(;r<n.length;)if(o=n[r],h(o)){for(;a<o.index;)a++,"TEMPLATE"===c.nodeName&&(e.push(c),s.currentNode=c.content),null===(c=s.nextNode())&&(s.currentNode=e.pop(),c=s.nextNode());if("node"===o.type){const t=this.processor.handleTextExpression(this.options);t.insertAfterNode(c.previousSibling),this.__parts.push(t)}else this.__parts.push(...this.processor.handleAttributeExpressions(c,o.name,o.strings,this.options));r++}else this.__parts.push(void 0),r++;return i&&(document.adoptNode(t),customElements.upgrade(t)),t}}
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const g=` ${a} `;class _{constructor(t,e,n,i){this.strings=t,this.values=e,this.type=n,this.processor=i}getHTML(){const t=this.strings.length-1;let e="",n=!1;for(let i=0;i<t;i++){const t=this.strings[i],s=t.lastIndexOf("\x3c!--");n=(s>-1||n)&&-1===t.indexOf("--\x3e",s+1);const o=m.exec(t);e+=null===o?t+(n?g:c):t.substr(0,o.index)+o[1]+o[2]+"$lit$"+o[3]+a}return e+=this.strings[t],e}getTemplateElement(){const t=document.createElement("template");return t.innerHTML=this.getHTML(),t}}
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const y=t=>null===t||!("object"==typeof t||"function"==typeof t),v=t=>Array.isArray(t)||!(!t||!t[Symbol.iterator]);class w{constructor(t,e,n){this.dirty=!0,this.element=t,this.name=e,this.strings=n,this.parts=[];for(let t=0;t<n.length-1;t++)this.parts[t]=this._createPart()}_createPart(){return new b(this)}_getValue(){const t=this.strings,e=t.length-1;let n="";for(let i=0;i<e;i++){n+=t[i];const e=this.parts[i];if(void 0!==e){const t=e.value;if(y(t)||!v(t))n+="string"==typeof t?t:String(t);else for(const e of t)n+="string"==typeof e?e:String(e)}}return n+=t[e],n}commit(){this.dirty&&(this.dirty=!1,this.element.setAttribute(this.name,this._getValue()))}}class b{constructor(t){this.value=void 0,this.committer=t}setValue(t){t===o||y(t)&&t===this.value||(this.value=t,n(t)||(this.committer.dirty=!0))}commit(){for(;n(this.value);){const t=this.value;this.value=o,t(this)}this.value!==o&&this.committer.commit()}}class S{constructor(t){this.value=void 0,this.__pendingValue=void 0,this.options=t}appendInto(t){this.startNode=t.appendChild(p()),this.endNode=t.appendChild(p())}insertAfterNode(t){this.startNode=t,this.endNode=t.nextSibling}appendIntoPart(t){t.__insert(this.startNode=p()),t.__insert(this.endNode=p())}insertAfterPart(t){t.__insert(this.startNode=p()),this.endNode=t.endNode,t.endNode=this.startNode}setValue(t){this.__pendingValue=t}commit(){for(;n(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=o,t(this)}const t=this.__pendingValue;t!==o&&(y(t)?t!==this.value&&this.__commitText(t):t instanceof _?this.__commitTemplateResult(t):t instanceof Node?this.__commitNode(t):v(t)?this.__commitIterable(t):t===r?(this.value=r,this.clear()):this.__commitText(t))}__insert(t){this.endNode.parentNode.insertBefore(t,this.endNode)}__commitNode(t){this.value!==t&&(this.clear(),this.__insert(t),this.value=t)}__commitText(t){const e=this.startNode.nextSibling,n="string"==typeof(t=null==t?"":t)?t:String(t);e===this.endNode.previousSibling&&3===e.nodeType?e.data=n:this.__commitNode(document.createTextNode(n)),this.value=t}__commitTemplateResult(t){const e=this.options.templateFactory(t);if(this.value instanceof f&&this.value.template===e)this.value.update(t.values);else{const n=new f(e,t.processor,this.options),i=n._clone();n.update(t.values),this.__commitNode(i),this.value=n}}__commitIterable(t){Array.isArray(this.value)||(this.value=[],this.clear());const e=this.value;let n,i=0;for(const s of t)n=e[i],void 0===n&&(n=new S(this.options),e.push(n),0===i?n.appendIntoPart(this):n.insertAfterPart(e[i-1])),n.setValue(s),n.commit(),i++;i<e.length&&(e.length=i,this.clear(n&&n.endNode))}clear(t=this.startNode){s(this.startNode.parentNode,t.nextSibling,this.endNode)}}class x{constructor(t,e,n){if(this.value=void 0,this.__pendingValue=void 0,2!==n.length||""!==n[0]||""!==n[1])throw new Error("Boolean attributes can only contain a single expression");this.element=t,this.name=e,this.strings=n}setValue(t){this.__pendingValue=t}commit(){for(;n(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=o,t(this)}if(this.__pendingValue===o)return;const t=!!this.__pendingValue;this.value!==t&&(t?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name),this.value=t),this.__pendingValue=o}}class P extends w{constructor(t,e,n){super(t,e,n),this.single=2===n.length&&""===n[0]&&""===n[1]}_createPart(){return new C(this)}_getValue(){return this.single?this.parts[0].value:super._getValue()}commit(){this.dirty&&(this.dirty=!1,this.element[this.name]=this._getValue())}}class C extends b{}let M=!1;try{const t={get capture(){return M=!0,!1}};window.addEventListener("test",t,t),window.removeEventListener("test",t,t)}catch(t){}class N{constructor(t,e,n){this.value=void 0,this.__pendingValue=void 0,this.element=t,this.eventName=e,this.eventContext=n,this.__boundHandleEvent=t=>this.handleEvent(t)}setValue(t){this.__pendingValue=t}commit(){for(;n(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=o,t(this)}if(this.__pendingValue===o)return;const t=this.__pendingValue,e=this.value,i=null==t||null!=e&&(t.capture!==e.capture||t.once!==e.once||t.passive!==e.passive),s=null!=t&&(null==e||i);i&&this.element.removeEventListener(this.eventName,this.__boundHandleEvent,this.__options),s&&(this.__options=E(t),this.element.addEventListener(this.eventName,this.__boundHandleEvent,this.__options)),this.value=t,this.__pendingValue=o}handleEvent(t){"function"==typeof this.value?this.value.call(this.eventContext||this.element,t):this.value.handleEvent(t)}}const E=t=>t&&(M?{capture:t.capture,passive:t.passive,once:t.once}:t.capture)
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */;const T=new class{handleAttributeExpressions(t,e,n,i){const s=e[0];if("."===s){return new P(t,e.slice(1),n).parts}return"@"===s?[new N(t,e.slice(1),i.eventContext)]:"?"===s?[new x(t,e.slice(1),n)]:new w(t,e,n).parts}handleTextExpression(t){return new S(t)}};
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */function A(t){let e=k.get(t.type);void 0===e&&(e={stringsArray:new WeakMap,keyString:new Map},k.set(t.type,e));let n=e.stringsArray.get(t.strings);if(void 0!==n)return n;const i=t.strings.join(a);return n=e.keyString.get(i),void 0===n&&(n=new d(t,t.getTemplateElement()),e.keyString.set(i,n)),e.stringsArray.set(t.strings,n),n}const k=new Map,D=new WeakMap;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
(window.litHtmlVersions||(window.litHtmlVersions=[])).push("1.1.2");const $=(t,...e)=>new _(t,e,"html",T)
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */;function H(t,e){const{element:{content:n},parts:i}=t,s=document.createTreeWalker(n,133,null,!1);let o=V(i),r=i[o],a=-1,c=0;const l=[];let d=null;for(;s.nextNode();){a++;const t=s.currentNode;for(t.previousSibling===d&&(d=null),e.has(t)&&(l.push(t),null===d&&(d=t)),null!==d&&c++;void 0!==r&&r.index===a;)r.index=null!==d?-1:r.index-c,o=V(i,o),r=i[o]}l.forEach(t=>t.parentNode.removeChild(t))}const O=t=>{let e=11===t.nodeType?0:1;const n=document.createTreeWalker(t,133,null,!1);for(;n.nextNode();)e++;return e},V=(t,e=-1)=>{for(let n=e+1;n<t.length;n++){const e=t[n];if(h(e))return n}return-1};
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const Y=(t,e)=>`${t}--${e}`;let R=!0;void 0===window.ShadyCSS?R=!1:void 0===window.ShadyCSS.prepareTemplateDom&&(console.warn("Incompatible ShadyCSS version detected. Please update to at least @webcomponents/webcomponentsjs@2.0.2 and @webcomponents/shadycss@1.3.1."),R=!1);const U=t=>e=>{const n=Y(e.type,t);let i=k.get(n);void 0===i&&(i={stringsArray:new WeakMap,keyString:new Map},k.set(n,i));let s=i.stringsArray.get(e.strings);if(void 0!==s)return s;const o=e.strings.join(a);if(s=i.keyString.get(o),void 0===s){const n=e.getTemplateElement();R&&window.ShadyCSS.prepareTemplateDom(n,t),s=new d(e,n),i.keyString.set(o,s)}return i.stringsArray.set(e.strings,s),s},L=["html","svg"],j=new Set,z=(t,e,n)=>{j.add(t);const i=n?n.element:document.createElement("template"),s=e.querySelectorAll("style"),{length:o}=s;if(0===o)return void window.ShadyCSS.prepareTemplateStyles(i,t);const r=document.createElement("style");for(let t=0;t<o;t++){const e=s[t];e.parentNode.removeChild(e),r.textContent+=e.textContent}(t=>{L.forEach(e=>{const n=k.get(Y(e,t));void 0!==n&&n.keyString.forEach(t=>{const{element:{content:e}}=t,n=new Set;Array.from(e.querySelectorAll("style")).forEach(t=>{n.add(t)}),H(t,n)})})})(t);const a=i.content;n?function(t,e,n=null){const{element:{content:i},parts:s}=t;if(null==n)return void i.appendChild(e);const o=document.createTreeWalker(i,133,null,!1);let r=V(s),a=0,c=-1;for(;o.nextNode();){for(c++,o.currentNode===n&&(a=O(e),n.parentNode.insertBefore(e,n));-1!==r&&s[r].index===c;){if(a>0){for(;-1!==r;)s[r].index+=a,r=V(s,r);return}r=V(s,r)}}}(n,r,a.firstChild):a.insertBefore(r,a.firstChild),window.ShadyCSS.prepareTemplateStyles(i,t);const c=a.querySelector("style");if(window.ShadyCSS.nativeShadow&&null!==c)e.insertBefore(c.cloneNode(!0),e.firstChild);else if(n){a.insertBefore(r,a.firstChild);const t=new Set;t.add(r),H(n,t)}};window.JSCompiler_renameProperty=(t,e)=>t;const I={toAttribute(t,e){switch(e){case Boolean:return t?"":null;case Object:case Array:return null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){switch(e){case Boolean:return null!==t;case Number:return null===t?null:Number(t);case Object:case Array:return JSON.parse(t)}return t}},F=(t,e)=>e!==t&&(e==e||t==t),q={attribute:!0,type:String,converter:I,reflect:!1,hasChanged:F},B=Promise.resolve(!0);class W extends HTMLElement{constructor(){super(),this._updateState=0,this._instanceProperties=void 0,this._updatePromise=B,this._hasConnectedResolver=void 0,this._changedProperties=new Map,this._reflectingProperties=void 0,this.initialize()}static get observedAttributes(){this.finalize();const t=[];return this._classProperties.forEach((e,n)=>{const i=this._attributeNameForProperty(n,e);void 0!==i&&(this._attributeToPropertyMap.set(i,n),t.push(i))}),t}static _ensureClassProperties(){if(!this.hasOwnProperty(JSCompiler_renameProperty("_classProperties",this))){this._classProperties=new Map;const t=Object.getPrototypeOf(this)._classProperties;void 0!==t&&t.forEach((t,e)=>this._classProperties.set(e,t))}}static createProperty(t,e=q){if(this._ensureClassProperties(),this._classProperties.set(t,e),e.noAccessor||this.prototype.hasOwnProperty(t))return;const n="symbol"==typeof t?Symbol():`__${t}`;Object.defineProperty(this.prototype,t,{get(){return this[n]},set(e){const i=this[t];this[n]=e,this._requestUpdate(t,i)},configurable:!0,enumerable:!0})}static finalize(){const t=Object.getPrototypeOf(this);if(t.hasOwnProperty("finalized")||t.finalize(),this.finalized=!0,this._ensureClassProperties(),this._attributeToPropertyMap=new Map,this.hasOwnProperty(JSCompiler_renameProperty("properties",this))){const t=this.properties,e=[...Object.getOwnPropertyNames(t),..."function"==typeof Object.getOwnPropertySymbols?Object.getOwnPropertySymbols(t):[]];for(const n of e)this.createProperty(n,t[n])}}static _attributeNameForProperty(t,e){const n=e.attribute;return!1===n?void 0:"string"==typeof n?n:"string"==typeof t?t.toLowerCase():void 0}static _valueHasChanged(t,e,n=F){return n(t,e)}static _propertyValueFromAttribute(t,e){const n=e.type,i=e.converter||I,s="function"==typeof i?i:i.fromAttribute;return s?s(t,n):t}static _propertyValueToAttribute(t,e){if(void 0===e.reflect)return;const n=e.type,i=e.converter;return(i&&i.toAttribute||I.toAttribute)(t,n)}initialize(){this._saveInstanceProperties(),this._requestUpdate()}_saveInstanceProperties(){this.constructor._classProperties.forEach((t,e)=>{if(this.hasOwnProperty(e)){const t=this[e];delete this[e],this._instanceProperties||(this._instanceProperties=new Map),this._instanceProperties.set(e,t)}})}_applyInstanceProperties(){this._instanceProperties.forEach((t,e)=>this[e]=t),this._instanceProperties=void 0}connectedCallback(){this._updateState=32|this._updateState,this._hasConnectedResolver&&(this._hasConnectedResolver(),this._hasConnectedResolver=void 0)}disconnectedCallback(){}attributeChangedCallback(t,e,n){e!==n&&this._attributeToProperty(t,n)}_propertyToAttribute(t,e,n=q){const i=this.constructor,s=i._attributeNameForProperty(t,n);if(void 0!==s){const t=i._propertyValueToAttribute(e,n);if(void 0===t)return;this._updateState=8|this._updateState,null==t?this.removeAttribute(s):this.setAttribute(s,t),this._updateState=-9&this._updateState}}_attributeToProperty(t,e){if(8&this._updateState)return;const n=this.constructor,i=n._attributeToPropertyMap.get(t);if(void 0!==i){const t=n._classProperties.get(i)||q;this._updateState=16|this._updateState,this[i]=n._propertyValueFromAttribute(e,t),this._updateState=-17&this._updateState}}_requestUpdate(t,e){let n=!0;if(void 0!==t){const i=this.constructor,s=i._classProperties.get(t)||q;i._valueHasChanged(this[t],e,s.hasChanged)?(this._changedProperties.has(t)||this._changedProperties.set(t,e),!0!==s.reflect||16&this._updateState||(void 0===this._reflectingProperties&&(this._reflectingProperties=new Map),this._reflectingProperties.set(t,s))):n=!1}!this._hasRequestedUpdate&&n&&this._enqueueUpdate()}requestUpdate(t,e){return this._requestUpdate(t,e),this.updateComplete}async _enqueueUpdate(){let t,e;this._updateState=4|this._updateState;const n=this._updatePromise;this._updatePromise=new Promise((n,i)=>{t=n,e=i});try{await n}catch(t){}this._hasConnected||await new Promise(t=>this._hasConnectedResolver=t);try{const t=this.performUpdate();null!=t&&await t}catch(t){e(t)}t(!this._hasRequestedUpdate)}get _hasConnected(){return 32&this._updateState}get _hasRequestedUpdate(){return 4&this._updateState}get hasUpdated(){return 1&this._updateState}performUpdate(){this._instanceProperties&&this._applyInstanceProperties();let t=!1;const e=this._changedProperties;try{t=this.shouldUpdate(e),t&&this.update(e)}catch(e){throw t=!1,e}finally{this._markUpdated()}t&&(1&this._updateState||(this._updateState=1|this._updateState,this.firstUpdated(e)),this.updated(e))}_markUpdated(){this._changedProperties=new Map,this._updateState=-5&this._updateState}get updateComplete(){return this._getUpdateComplete()}_getUpdateComplete(){return this._updatePromise}shouldUpdate(t){return!0}update(t){void 0!==this._reflectingProperties&&this._reflectingProperties.size>0&&(this._reflectingProperties.forEach((t,e)=>this._propertyToAttribute(e,this[e],t)),this._reflectingProperties=void 0)}updated(t){}firstUpdated(t){}}W.finalized=!0;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const J=(t,e)=>"method"!==e.kind||!e.descriptor||"value"in e.descriptor?{kind:"field",key:Symbol(),placement:"own",descriptor:{},initializer(){"function"==typeof e.initializer&&(this[e.key]=e.initializer.call(this))},finisher(n){n.createProperty(e.key,t)}}:Object.assign({},e,{finisher(n){n.createProperty(e.key,t)}});function Z(t){return(e,n)=>void 0!==n?((t,e,n)=>{e.constructor.createProperty(n,t)})(t,e,n):J(t,e)}
/**
@license
Copyright (c) 2019 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const X="adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,G=Symbol();class K{constructor(t,e){if(e!==G)throw new Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t}get styleSheet(){return void 0===this._styleSheet&&(X?(this._styleSheet=new CSSStyleSheet,this._styleSheet.replaceSync(this.cssText)):this._styleSheet=null),this._styleSheet}toString(){return this.cssText}}const Q=(t,...e)=>{const n=e.reduce((e,n,i)=>e+(t=>{if(t instanceof K)return t.cssText;if("number"==typeof t)return t;throw new Error(`Value passed to 'css' function must be a 'css' function result: ${t}. Use 'unsafeCSS' to pass non-literal values, but\n            take care to ensure page security.`)})(n)+t[i+1],t[0]);return new K(n,G)};
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
(window.litElementVersions||(window.litElementVersions=[])).push("2.2.1");const tt=t=>t.flat?t.flat(1/0):function t(e,n=[]){for(let i=0,s=e.length;i<s;i++){const s=e[i];Array.isArray(s)?t(s,n):n.push(s)}return n}(t);class et extends W{static finalize(){super.finalize.call(this),this._styles=this.hasOwnProperty(JSCompiler_renameProperty("styles",this))?this._getUniqueStyles():this._styles||[]}static _getUniqueStyles(){const t=this.styles,e=[];if(Array.isArray(t)){tt(t).reduceRight((t,e)=>(t.add(e),t),new Set).forEach(t=>e.unshift(t))}else t&&e.push(t);return e}initialize(){super.initialize(),this.renderRoot=this.createRenderRoot(),window.ShadowRoot&&this.renderRoot instanceof window.ShadowRoot&&this.adoptStyles()}createRenderRoot(){return this.attachShadow({mode:"open"})}adoptStyles(){const t=this.constructor._styles;0!==t.length&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow?X?this.renderRoot.adoptedStyleSheets=t.map(t=>t.styleSheet):this._needsShimAdoptedStyleSheets=!0:window.ShadyCSS.ScopingShim.prepareAdoptedCssText(t.map(t=>t.cssText),this.localName))}connectedCallback(){super.connectedCallback(),this.hasUpdated&&void 0!==window.ShadyCSS&&window.ShadyCSS.styleElement(this)}update(t){super.update(t);const e=this.render();e instanceof _&&this.constructor.render(e,this.renderRoot,{scopeName:this.localName,eventContext:this}),this._needsShimAdoptedStyleSheets&&(this._needsShimAdoptedStyleSheets=!1,this.constructor._styles.forEach(t=>{const e=document.createElement("style");e.textContent=t.cssText,this.renderRoot.appendChild(e)}))}render(){}}et.finalized=!0,et.render=(t,e,n)=>{if(!n||"object"!=typeof n||!n.scopeName)throw new Error("The `scopeName` option is required.");const i=n.scopeName,o=D.has(e),r=R&&11===e.nodeType&&!!e.host,a=r&&!j.has(i),c=a?document.createDocumentFragment():e;if(((t,e,n)=>{let i=D.get(e);void 0===i&&(s(e,e.firstChild),D.set(e,i=new S(Object.assign({templateFactory:A},n))),i.appendInto(e)),i.setValue(t),i.commit()})(t,c,Object.assign({templateFactory:U(i)},n)),a){const t=D.get(c);D.delete(c);const n=t.value instanceof f?t.value.template:void 0;z(i,c,n),s(e,e.firstChild),e.appendChild(c),D.set(e,t)}!o&&r&&window.ShadyCSS.styleElement(e.host)};var nt={},it=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,st="[^\\s]+",ot=/\[([^]*?)\]/gm,rt=function(){};function at(t,e){for(var n=[],i=0,s=t.length;i<s;i++)n.push(t[i].substr(0,e));return n}function ct(t){return function(e,n,i){var s=i[t].indexOf(n.charAt(0).toUpperCase()+n.substr(1).toLowerCase());~s&&(e.month=s)}}function lt(t,e){for(t=String(t),e=e||2;t.length<e;)t="0"+t;return t}var dt=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],ut=["January","February","March","April","May","June","July","August","September","October","November","December"],ht=at(ut,3),pt=at(dt,3);nt.i18n={dayNamesShort:pt,dayNames:dt,monthNamesShort:ht,monthNames:ut,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10)*t%10]}};var mt={D:function(t){return t.getDate()},DD:function(t){return lt(t.getDate())},Do:function(t,e){return e.DoFn(t.getDate())},d:function(t){return t.getDay()},dd:function(t){return lt(t.getDay())},ddd:function(t,e){return e.dayNamesShort[t.getDay()]},dddd:function(t,e){return e.dayNames[t.getDay()]},M:function(t){return t.getMonth()+1},MM:function(t){return lt(t.getMonth()+1)},MMM:function(t,e){return e.monthNamesShort[t.getMonth()]},MMMM:function(t,e){return e.monthNames[t.getMonth()]},YY:function(t){return lt(String(t.getFullYear()),4).substr(2)},YYYY:function(t){return lt(t.getFullYear(),4)},h:function(t){return t.getHours()%12||12},hh:function(t){return lt(t.getHours()%12||12)},H:function(t){return t.getHours()},HH:function(t){return lt(t.getHours())},m:function(t){return t.getMinutes()},mm:function(t){return lt(t.getMinutes())},s:function(t){return t.getSeconds()},ss:function(t){return lt(t.getSeconds())},S:function(t){return Math.round(t.getMilliseconds()/100)},SS:function(t){return lt(Math.round(t.getMilliseconds()/10),2)},SSS:function(t){return lt(t.getMilliseconds(),3)},a:function(t,e){return t.getHours()<12?e.amPm[0]:e.amPm[1]},A:function(t,e){return t.getHours()<12?e.amPm[0].toUpperCase():e.amPm[1].toUpperCase()},ZZ:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+lt(100*Math.floor(Math.abs(e)/60)+Math.abs(e)%60,4)}},ft={D:["\\d\\d?",function(t,e){t.day=e}],Do:["\\d\\d?"+st,function(t,e){t.day=parseInt(e,10)}],M:["\\d\\d?",function(t,e){t.month=e-1}],YY:["\\d\\d?",function(t,e){var n=+(""+(new Date).getFullYear()).substr(0,2);t.year=""+(e>68?n-1:n)+e}],h:["\\d\\d?",function(t,e){t.hour=e}],m:["\\d\\d?",function(t,e){t.minute=e}],s:["\\d\\d?",function(t,e){t.second=e}],YYYY:["\\d{4}",function(t,e){t.year=e}],S:["\\d",function(t,e){t.millisecond=100*e}],SS:["\\d{2}",function(t,e){t.millisecond=10*e}],SSS:["\\d{3}",function(t,e){t.millisecond=e}],d:["\\d\\d?",rt],ddd:[st,rt],MMM:[st,ct("monthNamesShort")],MMMM:[st,ct("monthNames")],a:[st,function(t,e,n){var i=e.toLowerCase();i===n.amPm[0]?t.isPm=!1:i===n.amPm[1]&&(t.isPm=!0)}],ZZ:["[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z",function(t,e){var n,i=(e+"").match(/([+-]|\d\d)/gi);i&&(n=60*i[1]+parseInt(i[2],10),t.timezoneOffset="+"===i[0]?n:-n)}]};ft.dd=ft.d,ft.dddd=ft.ddd,ft.DD=ft.D,ft.mm=ft.m,ft.hh=ft.H=ft.HH=ft.h,ft.MM=ft.M,ft.ss=ft.s,ft.A=ft.a,nt.masks={default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"},nt.format=function(t,e,n){var i=n||nt.i18n;if("number"==typeof t&&(t=new Date(t)),"[object Date]"!==Object.prototype.toString.call(t)||isNaN(t.getTime()))throw new Error("Invalid Date in fecha.format");e=nt.masks[e]||e||nt.masks.default;var s=[];return(e=(e=e.replace(ot,(function(t,e){return s.push(e),"@@@"}))).replace(it,(function(e){return e in mt?mt[e](t,i):e.slice(1,e.length-1)}))).replace(/@@@/g,(function(){return s.shift()}))},nt.parse=function(t,e,n){var i=n||nt.i18n;if("string"!=typeof e)throw new Error("Invalid format in fecha.parse");if(e=nt.masks[e]||e,t.length>1e3)return null;var s={},o=[],r=[];e=e.replace(ot,(function(t,e){return r.push(e),"@@@"}));var a,c=(a=e,a.replace(/[|\\{()[^$+*?.-]/g,"\\$&")).replace(it,(function(t){if(ft[t]){var e=ft[t];return o.push(e[1]),"("+e[0]+")"}return t}));c=c.replace(/@@@/g,(function(){return r.shift()}));var l=t.match(new RegExp(c,"i"));if(!l)return null;for(var d=1;d<l.length;d++)o[d-1](s,l[d],i);var u,h=new Date;return!0===s.isPm&&null!=s.hour&&12!=+s.hour?s.hour=+s.hour+12:!1===s.isPm&&12==+s.hour&&(s.hour=0),null!=s.timezoneOffset?(s.minute=+(s.minute||0)-+s.timezoneOffset,u=new Date(Date.UTC(s.year||h.getFullYear(),s.month||0,s.day||1,s.hour||0,s.minute||0,s.second||0,s.millisecond||0))):u=new Date(s.year||h.getFullYear(),s.month||0,s.day||1,s.hour||0,s.minute||0,s.second||0,s.millisecond||0),u};(function(){try{(new Date).toLocaleDateString("i")}catch(t){return"RangeError"===t.name}})(),function(){try{(new Date).toLocaleString("i")}catch(t){return"RangeError"===t.name}}(),function(){try{(new Date).toLocaleTimeString("i")}catch(t){return"RangeError"===t.name}}();var gt=["closed","locked","off"],_t=function(t,e,n,i){i=i||{},n=null==n?{}:n;var s=new Event(e,{bubbles:void 0===i.bubbles||i.bubbles,cancelable:Boolean(i.cancelable),composed:void 0===i.composed||i.composed});return s.detail=n,t.dispatchEvent(s),s},yt=new Set(["call-service","divider","section","weblink","cast","select"]),vt={alert:"toggle",automation:"toggle",climate:"climate",cover:"cover",fan:"toggle",group:"group",input_boolean:"toggle",input_number:"input-number",input_select:"input-select",input_text:"input-text",light:"toggle",lock:"lock",media_player:"media-player",remote:"toggle",scene:"scene",script:"script",sensor:"sensor",timer:"timer",switch:"toggle",vacuum:"toggle",water_heater:"climate",input_datetime:"input-datetime"},wt=function(t){_t(window,"haptic",t)},bt=function(t,e,n,i){var s;if("double_tap"===i&&n.double_tap_action?s=n.double_tap_action:"hold"===i&&n.hold_action?s=n.hold_action:"tap"===i&&n.tap_action&&(s=n.tap_action),s||(s={action:"more-info"}),!s.confirmation||s.confirmation.exemptions&&s.confirmation.exemptions.some((function(t){return t.user===e.user.id}))||(wt("warning"),confirm(s.confirmation.text||"Are you sure you want to "+s.action+"?")))switch(s.action){case"more-info":(n.entity||n.camera_image)&&_t(t,"hass-more-info",{entityId:n.entity?n.entity:n.camera_image});break;case"navigate":s.navigation_path&&function(t,e,n){void 0===n&&(n=!1),n?history.replaceState(null,"",e):history.pushState(null,"",e),_t(window,"location-changed",{replace:n})}(0,s.navigation_path);break;case"url":s.url_path&&window.open(s.url_path);break;case"toggle":n.entity&&(function(t,e){(function(t,e,n){void 0===n&&(n=!0);var i,s=function(t){return t.substr(0,t.indexOf("."))}(e),o="group"===s?"homeassistant":s;switch(s){case"lock":i=n?"unlock":"lock";break;case"cover":i=n?"open_cover":"close_cover";break;default:i=n?"turn_on":"turn_off"}t.callService(o,i,{entity_id:e})})(t,e,gt.includes(t.states[e].state))}(e,n.entity),wt("success"));break;case"call-service":if(!s.service)return void wt("failure");var o=s.service.split(".",2);e.callService(o[0],o[1],s.service_data),wt("success")}};function St(t){return void 0!==t&&"none"!==t.action}const xt="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0;class Pt extends HTMLElement{constructor(){super(),this.holdTime=500,this.ripple=document.createElement("mwc-ripple"),this.timer=void 0,this.held=!1,this.cooldownStart=!1,this.cooldownEnd=!1}connectedCallback(){Object.assign(this.style,{position:"absolute",width:xt?"100px":"50px",height:xt?"100px":"50px",transform:"translate(-50%, -50%)",pointerEvents:"none"}),this.appendChild(this.ripple),this.ripple.primary=!0,["touchcancel","mouseout","mouseup","touchmove","mousewheel","wheel","scroll"].forEach(t=>{document.addEventListener(t,()=>{clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0},{passive:!0})})}bind(t,e){if(t.actionHandler)return;t.actionHandler=!0,t.addEventListener("contextmenu",t=>{const e=t||window.event;e.preventDefault&&e.preventDefault(),e.stopPropagation&&e.stopPropagation(),e.cancelBubble=!0,e.returnValue=!1});const n=t=>{if(this.cooldownStart)return;let e,n;this.held=!1,t.touches?(e=t.touches[0].pageX,n=t.touches[0].pageY):(e=t.pageX,n=t.pageY),this.timer=window.setTimeout(()=>{this.startAnimation(e,n),this.held=!0},this.holdTime),this.cooldownStart=!0,window.setTimeout(()=>this.cooldownStart=!1,100)},i=n=>{this.cooldownEnd||["touchend","touchcancel"].includes(n.type)&&void 0===this.timer||(clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0,this.held?_t(t,"action",{action:"hold"}):e.hasDoubleTap?1===n.detail||"keyup"===n.type?this.dblClickTimeout=window.setTimeout(()=>{_t(t,"action",{action:"tap"})},250):(clearTimeout(this.dblClickTimeout),_t(t,"action",{action:"double_tap"})):_t(t,"action",{action:"tap"}),this.cooldownEnd=!0,window.setTimeout(()=>this.cooldownEnd=!1,100))};t.addEventListener("touchstart",n,{passive:!0}),t.addEventListener("touchend",i),t.addEventListener("touchcancel",i),t.addEventListener("keyup",t=>{if(13===t.keyCode)return i(t)}),/iPhone OS 13_/.test(window.navigator.userAgent)||(t.addEventListener("mousedown",n,{passive:!0}),t.addEventListener("click",i))}startAnimation(t,e){Object.assign(this.style,{left:`${t}px`,top:`${e}px`,display:null}),this.ripple.disabled=!1,this.ripple.active=!0,this.ripple.unbounded=!0}stopAnimation(){this.ripple.active=!1,this.ripple.disabled=!0,this.style.display="none"}}customElements.define("action-handler-radial",Pt);const Ct=(t,e)=>{const n=(()=>{const t=document.body;if(t.querySelector("action-handler-radial"))return t.querySelector("action-handler-radial");const e=document.createElement("action-handler-radial");return t.appendChild(e),e})();n&&n.bind(t,e)},Mt=(Nt=(t={})=>e=>{Ct(e.committer.element,t)},(...t)=>{const n=Nt(...t);return e.set(n,!0),n});var Nt;console.info("%c  RADIAL-MENU   \n%c  Version 1.5.0 ","color: orange; font-weight: bold; background: black","color: white; font-weight: bold; background: dimgray");let Et=class extends et{setConfig(t){if(!t)throw new Error("Invalid configuration");if(!t.items)throw new Error("Invalid configuration: No items defined");this._config=Object.assign({icon:"mdi:menu",name:"menu",tap_action:{action:"toggle-menu"},hold_action:{action:"none"},double_tap_action:{action:"none"},default_dismiss:!0},t),this.loadCardHelpers()}getCardSize(){return 1}render(){return this._config&&this.hass?(this._config.items.forEach(t=>{t.card&&(t.element=this._helpers?this._helpers.createCardElement(t.card):function(t,e){void 0===e&&(e=!1);var n=function(t,e){return i("hui-error-card",{type:"error",error:t,config:e})},i=function(t,e){var i=window.document.createElement(t);try{i.setConfig(e)}catch(i){return console.error(t,i),n(i.message,e)}return i};if(!t||"object"!=typeof t||!e&&!t.type)return n("No type defined",t);var s=t.type;if(s&&s.startsWith("custom:"))s=s.substr("custom:".length);else if(e)if(yt.has(s))s="hui-"+s+"-row";else{if(!t.entity)return n("Invalid config given.",t);var o=t.entity.split(".",1)[0];s="hui-"+(vt[o]||"text")+"-entity-row"}else s="hui-"+s+"-card";if(customElements.get(s))return i(s,t);var r=n("Custom element doesn't exist: "+t.type+".",t);r.style.display="None";var a=setTimeout((function(){r.style.display=""}),2e3);return customElements.whenDefined(t.type).then((function(){clearTimeout(a),_t(r,"ll-rebuild",{},r)})),r}(t.card),t.element&&(t.element.hass=this.hass,t.element.classList.add("custom")))}),$`
      <nav class="circular-menu">
        <div class="circle">
          ${this._config.items.map((t,e)=>{const n=this._config?(50-35*Math.cos(-.5*Math.PI-1/this._config.items.length*2*e*Math.PI)).toFixed(4)+"%":"",i=this._config?(50+35*Math.sin(-.5*Math.PI-1/this._config.items.length*2*e*Math.PI)).toFixed(4)+"%":"";return t.card&&t.element&&(t.element.style.setProperty("left",n),t.element.style.setProperty("top",i)),t.entity_picture?$`
                  <state-badge
                    @action=${this._handleAction}
                    .actionHandler=${Mt({hasHold:St(t.hold_action),hasDoubleTap:St(t.double_tap_action)})}
                    .config=${t}
                    .stateObj=${{attributes:{entity_picture:t.entity_picture},entity_id:"sensor.fake"}}
                    style="
                left:${n};
                top:${i};"
                  ></state-badge>
                `:t.card?t.element:$`
                  <ha-icon
                    @action=${this._handleAction}
                    .actionHandler=${Mt({hasHold:St(t.hold_action),hasDoubleTap:St(t.double_tap_action)})}
                    .config=${t}
                    .icon=${t.icon}
                    .title=${t.name}
                    style="
                left:${n};
                top:${i};"
                  ></ha-icon>
                `})}
        </div>
        ${this._config.entity_picture?$`
              <state-badge
                class="menu-button"
                .menu=${!0}
                @action=${this._handleAction}
                .actionHandler=${Mt({hasHold:St(this._config.hold_action),hasDoubleTap:St(this._config.double_tap_action)})}
                .config=${this._config}
                .stateObj=${{attributes:{entity_picture:this._config.entity_picture},entity_id:"sensor.fake"}}
              ></state-badge>
            `:$`
              <ha-icon
                class="menu-button"
                .menu=${!0}
                @action=${this._handleAction}
                .actionHandler=${Mt({hasHold:St(this._config.hold_action),hasDoubleTap:St(this._config.double_tap_action)})}
                .icon=${this._config.icon}
                .title=${this._config.name}
                .config=${this._config}
              ></ha-icon>
            `}
      </nav>
    `):$``}firstUpdated(){this._config&&this._config.default_open&&this._toggleMenu()}_toggleMenu(){if(this.shadowRoot){const t=this.shadowRoot.querySelector(".circle");t&&t.classList.toggle("open")}}async loadCardHelpers(){this._helpers=await window.loadCardHelpers()}_handleAction(t){const e=t.target.config;e&&t.detail.action&&("tap"===t.detail.action&&e.tap_action&&"toggle-menu"===e.tap_action.action||"hold"===t.detail.action&&e.hold_action&&"toggle-menu"===e.hold_action.action||"double_tap"===t.detail.action&&e.double_tap_action&&"toggle-menu"===e.double_tap_action.action)?this._toggleMenu():(this.hass&&t.detail.action&&bt(this,this.hass,e,t.detail.action),this._config&&this._config.default_dismiss&&!t.target.menu&&this._toggleMenu())}static get styles(){return Q`
      .circular-menu {
        width: 250px;
        height: 250px;
        margin: 0 auto;
        position: relative;
      }

      .circle {
        width: 250px;
        height: 250px;
        opacity: 0;

        -webkit-transform: scale(0);
        -moz-transform: scale(0);
        transform: scale(0);

        -webkit-transition: all 0.4s ease-out;
        -moz-transition: all 0.4s ease-out;
        transition: all 0.4s ease-out;
      }

      .open.circle {
        opacity: 1;
        -webkit-transform: scale(1);
        -moz-transform: scale(1);
        transform: scale(1);
      }

      .circle ha-icon,
      .circle state-badge,
      .custom {
        display: block;
        position: absolute;
      }

      .custom {
        height: 100px;
        width: 100px;
        margin-left: -40px;
        margin-top: -25px;
      }

      .circle ha-icon,
      .circle state-badge {
        text-decoration: none;
        border-radius: 50%;
        text-align: center;
        height: 40px;
        width: 40px;
        line-height: 40px;
        margin-left: -20px;
        margin-top: -20px;
      }

      .circle ha-icon:hover {
        color: var(--accent-color);
      }

      .circle state-badge:hover {
        background-color: var(--secondary-background-color);
      }

      ha-icon,
      state-badge {
        cursor: pointer;
        color: var(--primary-color);
      }

      ha-icon {
        cursor: pointer;
      }

      .menu-button {
        position: absolute;
        text-decoration: none;
        text-align: center;
        border-radius: 50%;
        display: block;
        height: 40px;
        width: 40px;
        line-height: 40px;
      }

      state-badge.menu-button {
        top: calc(50% - 20px);
        left: calc(50% - 20px);
      }

      ha-icon.menu-button {
        top: calc(50% - 30px);
        left: calc(50% - 30px);
        padding: 10px;
      }

      .menu-button:hover {
        background-color: var(--secondary-background-color);
      }
    `}};var Tt;t([Z()],Et.prototype,"hass",void 0),t([Z()],Et.prototype,"_config",void 0),t([Z()],Et.prototype,"_helpers",void 0),Et=t([(Tt="radial-menu",t=>"function"==typeof t?((t,e)=>(window.customElements.define(t,e),e))(Tt,t):((t,e)=>{const{kind:n,elements:i}=e;return{kind:n,elements:i,finisher(e){window.customElements.define(t,e)}}})(Tt,t))],Et);export{Et as RadialMenu};
