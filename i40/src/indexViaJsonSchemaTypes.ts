import { Asset, AssetAdministrationShell, ModelType } from "./lib/AasJsonSchemaTypes";
import { Util } from "./util/Util";

const myAssetId = "myAssetId";
const myAsset: Asset = {
    idShort: myAssetId,
    identification: {
        id: Util.hash(myAssetId),
        idType: "IRDI"
    },
    modelType: {
        name: "Asset"
    },
    kind: "Instance"
};

const myAasId = "myAasId";
const myAas: AssetAdministrationShell = {
    asset: {
        keys: [{
            idType: "IRDI",
            local: true,
            type: "Asset",
            value: Util.hash(myAssetId)
        }]
    },
    conceptDictionaries: [],
    idShort: myAasId,
    identification: {
        id: Util.hash(myAasId),
        idType: "IRDI"
    },
    modelType: {
        name: "AssetAdministrationShell"
    }
}

console.log(JSON.stringify(myAas, null, 4));