/* tslint:disable */
/* eslint-disable */
/**
 * Gym Store
 * Test Store to Sell Gym Clothes
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import type { Price } from './Price';
import {
    PriceFromJSON,
    PriceFromJSONTyped,
    PriceToJSON,
} from './Price';

/**
 * 
 * @export
 * @interface SubscriptionItem
 */
export interface SubscriptionItem {
    /**
     * 
     * @type {string}
     * @memberof SubscriptionItem
     */
    id: string;
    /**
     * 
     * @type {Price}
     * @memberof SubscriptionItem
     */
    price: Price;
    /**
     * The quantity of the plan to which the customer should be subscribed.
     * @type {number}
     * @memberof SubscriptionItem
     */
    quantity?: number | null;
}

/**
 * Check if a given object implements the SubscriptionItem interface.
 */
export function instanceOfSubscriptionItem(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "price" in value;

    return isInstance;
}

export function SubscriptionItemFromJSON(json: any): SubscriptionItem {
    return SubscriptionItemFromJSONTyped(json, false);
}

export function SubscriptionItemFromJSONTyped(json: any, ignoreDiscriminator: boolean): SubscriptionItem {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'price': PriceFromJSON(json['price']),
        'quantity': !exists(json, 'quantity') ? undefined : json['quantity'],
    };
}

export function SubscriptionItemToJSON(value?: SubscriptionItem | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'price': PriceToJSON(value.price),
        'quantity': value.quantity,
    };
}

