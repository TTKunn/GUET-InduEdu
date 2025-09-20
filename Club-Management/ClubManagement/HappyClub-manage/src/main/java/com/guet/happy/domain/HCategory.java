package com.guet.happy.domain;

import lombok.Data;

@Data
public class HCategory {
    private Integer categoryId; // category_id
    private String name; // name
    private String description; // description
    private java.util.Date deletedAt; // deleted_at
}
