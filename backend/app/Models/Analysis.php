<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Analysis extends Model
{
    protected $fillable = [
        'patient_id',
        'user_id',
        'image_path',
        'heatmap_path',
        'label'
    ];
}
