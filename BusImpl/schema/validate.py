import json

from jsonschema import RefResolver, Draft7Validator

schema_store = {}
for file in ["bus.schema.json", "player.bus.schema.json", "workerarea.bus.schema.json"]:
   schema = json.load(open(file))
   schema_store[schema["$id"]] = schema

print(schema_store.keys())

resolver = RefResolver.from_schema(schema, store=schema_store)
validator = Draft7Validator(schema_store["https://schema.theboardgame.party/bus.schema.json"], resolver=resolver)

busState = json.load(open("sample_state.json"))
print(validator.validate(busState))
