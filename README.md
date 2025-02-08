# Usage

## Running Visual fidelity test

```shell
npx @animaapp/scooby-cli fidelity \
  --name "fidelity-name" \
  --expected full-path/expected \
  --actual full-path/actual \
  --file-type=png
```

## Visualizing Visual fidelity test
- Unzip `fidelity-name.zip` 
- Execute `jsonParser.py`
- Should see 'report.json'

## Interpreting the results from Visual fidelity test with LLM (Step 1 - Finding the unmatched elements)
- Upload `extracted_images/image_2.png` with the following prompt
```text
You are a UI/UX master
image_2.png consists of highlight of mismatched elements (in brighter red) from the figma design as compared to actual implementation. Whatever in opaque are matched design.

Pls find and list down the elements that are highlighted and you're certain about for the next agent that has access to the codebase and figma to find out the exact properties mismatched.

Pls dont make up something does not highlighted.
```

## Interpreting the results from Visual fidelity test with LLM (Step 2 (Optional) - Finding the impacted code)
- Required context from codebase, figma API
```text
The previous agent has identified these mismatch elements (Captured on live website) from expected figma design, please find and return only the relavant code  by using the figma data and the code given. 

Previous agent results:

Figma:

Code:
```