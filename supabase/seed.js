import * as fs from 'fs';
import * as util from 'util';
import * as path from 'path';
import * as child_process from 'child_process'; 
import mime from 'mime';
import 'dotenv/config';
import { createClient } from '@supabase/supabase-js';

const exec = util.promisify(child_process.exec);

const { stdout: supabaseStatus } = await exec('npx supabase status -o json');
const supabaseEnv = JSON.parse(supabaseStatus);

const supabase = createClient(
  supabaseEnv.API_URL,
  supabaseEnv.SERVICE_ROLE_KEY,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    },
  },
);

const walkDir = (dir, callback) => {
  fs.readdirSync(dir).forEach( f => {
    let dirPath = path.join(dir, f);
    let isDirectory = fs.statSync(dirPath).isDirectory();
    isDirectory ? 
      walkDir(dirPath, callback) : callback(path.join(dir, f));
  });
};

const uploadFile = (bucketName, filePath, fileData, options) => {
  const { error } = supabase.storage
    .from(bucketName)
    .upload(filePath, fileData, options);

  if (error) throw error;

  console.log(`File uploaded to ${bucketName}:${filePath}`);
};

const storagePath = 'storage/';

fs.readdir(storagePath, (err, buckets) => {
  buckets.forEach((bucket) => {
    const bucketPath = path.join(storagePath, bucket);
    
    walkDir(bucketPath, (filePath) => {
      const uploadPath = path.join(...filePath.split('/').slice(2));
      const mimeType = mime.getType(filePath);
      
      fs.readFile(filePath, (err, data) => {
        if (err) {
          console.error(err);
          return;
        }

        uploadFile(bucket, uploadPath, data, {
          contentType: mimeType,
        });
      });
    });
  });
});
