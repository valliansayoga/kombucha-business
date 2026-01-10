```mermaid
flowchart TD
A((Start))
B{Change Price}
C[Update]
D[No Update]
E[Insert Current Timestamp]
END((End))
A --> B
B --[Yes]--> C --> E --> END
B --[No]--> D --> END
```