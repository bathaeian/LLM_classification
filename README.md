<OL>
  <LI>
    Download OMNIGLOT dataset from this site
<br>
https://github.com/pengsuhua/PMF_OMNIGLOT/tree/main/data
  </LI>
  <LI>
    extract data
  </LI>
  <LI>
    Enter this command
    <br>
    python image_to_pointcloud_small.py --input "./PMF_OMNIGLOT-main/PMF_OMNIGLOT-main/data/train" --output "./data/train/xsmall/nothin/" --resize 25 --no-thin
  </LI>
  <LI>
    Enter this command
    <br>
python export_dataset3.py --input "./data/test/small20/border_noise/0/0/" --output "./data/test/border_noise/0/bn0.json"
  </LI>
</OL>


