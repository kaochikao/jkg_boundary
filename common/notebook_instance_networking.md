


- Glue notebook 一定需要internet去access dev endpoint嗎？
    - 但沒有inet access, Livy能找到dev endpoint嗎？ 
        - 應該可以，DevEnd也有時只有private DNS, private IP.
    - 跟DevEndpoint應該不用internet可以講話，跟Service講話可以用VPC endpoints (SM interface endpoint, Glue interface endpoint, S3 gateway endpoint)
- Glue console沒有選項，那default是什麼？
    - Glue console 產生的都是internet access enabled.
- 是否其實可以用subnet去限制，有無internet access不重要?
    - 不行，建了一個nb instance到一個private subnet, 沒有NAT, 一樣可以wget, 應該是在service VPC端有另外的網卡
    - ifconfig出來確實有很多網卡 
