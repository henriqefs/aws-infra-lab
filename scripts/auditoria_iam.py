import boto3
from datetime import datetime, timezone

iam = boto3.client("iam")
achados = 0

for page in iam.get_paginator("list_users").paginate():
    for user in page["Users"]:
        nome = user["UserName"]
        if not iam.list_mfa_devices(UserName=nome)["MFADevices"]:
            print(f"[SEM MFA] {nome}")
            achados += 1
        for key in iam.list_access_keys(UserName=nome)["AccessKeyMetadata"]:
            idade = (datetime.now(timezone.utc) - key["CreateDate"]).days
            if idade > 90:
                print(f"[CHAVE VELHA] {nome} - {key['AccessKeyId']} ({idade} dias)")
                achados += 1

print(f"Auditoria concluída: {achados} achado(s).")
