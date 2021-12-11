import { Asset, AssetAdministrationShell, AssetAdministrationShellEnv, IdTypeEnum } from "i40-aas-objects";
import { AssetKindEnum } from "i40-aas-objects/dist/src/types/AssetKindEnum";
import { Util } from "./util/Util";

// Create an asset
// IRDI: International Registration Data Identifier
const myAssetId = "myAssetId";
const myAsset = new Asset({ id: Util.hash(myAssetId), idType: IdTypeEnum.IRDI },
    myAssetId,
);
myAsset.kind = AssetKindEnum.Instance;
//myAsset.setAssetIdentificationModel(myAssetIdentificationModel.getReference());


// Create an AAS
const myAasId = "myAasId";
const myAas = new AssetAdministrationShell(
    { id: Util.hash(myAasId), idType: IdTypeEnum.IRDI },
    myAasId
);
myAas.setAsset(myAsset.getReference());

// Create an AAS Env
// An Env contains AAS, assets, submodels and conceptDescriptions
const myAasEnv = new AssetAdministrationShellEnv()
    .addAssetAdministrationShell(myAas)
    .addAsset(myAsset);

console.log(JSON.stringify(myAasEnv, null, 4));

